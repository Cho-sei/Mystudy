from pylsl import StreamInlet, resolve_stream, resolve_byprop,\
 	proc_clocksync, proc_dejitter, proc_monotonize
from psychopy import visual, event, core
from collections import deque
import numpy as np
import threading
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper
import itertools
import pandas as pd
import serial
import winsound
from streaming import BetaInlet
from record_baseline_every import baseline as bsl
from fatigue import fatigue_VAS
import csv
import sys
import os
import random
from trigger import trigger
from experiment_parameter import MIexperiment_components

def control_task(win, components, fmin, fmax, pid, day):
	condition_fname = 'result/' + pid + '_control_training.csv'
	fatigue_fname = 'result/' + pid + '_fatigue.csv'

	betaIn = BetaInlet()

	data_buffer = deque([], maxlen=components.N)	#ストリーミングデータ
	data_buffer_blink = deque([], maxlen=components.N)	#ストリーミングデータ
	summary = pd.DataFrame()
	pre_baseline = pd.DataFrame({'C4':[500], 'C3':[500]})

	#data_bufferの初期化
	while len(data_buffer) < components.N:	
		sample, timestamp = betaIn.update()
		if len(sample) != 0:
			ROI = components.channels['C4'] if components.df.iloc[[0]].hand.item() == 'left' else components.channels['C3']
			data_buffer.extend(sample.T[ROI])

	fatigue_res = []
	concentrate_res = []
	difficulty_res = []
	prediction_res = []

	#define dummy
	if day == 'Day1':
		dummy = components.dummyList[0]
	elif day == 'Day2':
		dummy = components.dummyList[1]
	else:
		dummy = components.dummyList[2]

	#display stimulus
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	for blocks in range(components.blockNum):

		ERSP_fname = 'result/' + pid + '_control_ERSP_' + day + '_b' + str(blocks) + '.csv'

		components.df['block'] = blocks

		RT = []
		for i, row in components.df.iterrows():

			if row['hand'] == 'left':

				trigger.SendTrigger('relax_left_b' + str(blocks+1))
				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				baseline = bsl(win, components, fmin, fmax, pid, day, blocks, i, pre_baseline)
				
				components.cue.setText('Left')
				components.cue.draw()
				win.flip()
				core.wait(components.cue_duration)
				trigger.SendTrigger('task_left_b' + str(blocks+1))
				components.fixation.draw()
				win.flip()

				ch = components.channels['C4']
				base = baseline['C4']

			else:

				trigger.SendTrigger('relax_right_b' + str(blocks+1))
				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				baseline = bsl(win, components, fmin, fmax, pid, day, blocks, i, pre_baseline)
				
				components.cue.setText('Right')
				components.cue.draw()
				win.flip()
				core.wait(components.cue_duration)
				trigger.SendTrigger('task_right_b' + str(blocks+1))
				components.fixation.draw()
				win.flip()

				ch = components.channels['C3']
				base = baseline['C3']

			clock = core.Clock()
			t_start = clock.getTime()
			t_duration = clock.getTime() - t_start

			j = 0
			pre_time = 0
			ERSP_List = []
			firstFlag = True
			waiting_key = True
			while waiting_key:
				sample, timestamp = betaIn.update()
				data_buffer.extend(sample.T[ch])
				data_buffer_blink.extend(sample.T[1])
				display_buffer = detrend(data_buffer)
				display_buffer_blink = detrend(data_buffer_blink)
				if any(display_buffer_blink > 100):
					if firstFlag:
						ERSP = 0
						firstFlag = False
					else:
						ERSP = pre_data
				else:
					psd, freqs = psd_array_multitaper(display_buffer, betaIn.sampling_rate(), fmin=fmin, fmax=fmax)
					ERSP = 100 * (np.average(psd) - base) / base
				ERSP_List.append(ERSP)

				components.Circle.setRadius(5*dummy[blocks][i][j] + 300)
				components.Circle.draw()
				components.fixation.draw()
				win.flip()

				if t_duration%0.1 < 0.02:
					if (t_duration - pre_time) > 0.05:
						j += 1
						pre_time = t_duration

				if j == len(dummy[blocks][i])-1:
					j = 0
				
				t_duration = clock.getTime() - t_start
				if 'return' in event.getKeys(keyList=['return']):
					RT.append(t_duration)
					waiting_key = False

				pre_data = ERSP

			with open(ERSP_fname, 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(ERSP_List)

			win.flip()
			core.wait(components.FB_duration + random.choice(components.wait_time_list))

		fatigue_return = fatigue_VAS(win, components)
		fatigue_res.append(fatigue_return[0])
		concentrate_res.append(fatigue_return[1])
		difficulty_res.append(fatigue_return[2])
		prediction_res.append(fatigue_return[3])
		components.rest(win, blocks+2)

		components.df['RT'] = RT
		summary = pd.concat([summary, components.df])

	fatigue_df = pd.DataFrame({'fatigue':fatigue_res, 
							   'concentrate':concentrate_res,
							   'difficulty':difficulty_res,
							   'prediction':prediction_res})
	fatigue_df.insert(0, 'block', range(components.blockNum))
	fatigue_df.insert(0, 'day', day)
	fatigue_df.insert(0, 'condition', 'control')
	fatigue_df.insert(0, 'pid', pid)

	summary.insert(0, 'day', day)
	summary.insert(0, 'condition', 'control')
	summary.insert(0, 'pid', pid)
	if day == 'Day1':
		summary.to_csv(condition_fname)
		fatigue_df.to_csv(fatigue_fname)
	else:
		if os.path.exists(fatigue_fname):
			fat_df = pd.read_csv(fatigue_fname, index_col=0)
			pd.concat([fat_df, fatigue_df], sort=False).to_csv(fatigue_fname)
		else:
			fatigue_df.to_csv(fatigue_fname)
		if os.path.exists(condition_fname):
			train_df = pd.read_csv(condition_fname, index_col=0)
			pd.concat([train_df, summary]).to_csv(condition_fname)
		else:
			summary.to_csv(condition_fname)


	core.wait(1)

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	control_task(win, components, fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2])

