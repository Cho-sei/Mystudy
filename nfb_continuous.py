"""Example program to show how to read a multi-channel time series from LSL."""

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
from record_baseline import baseline
import csv
import sys
import os
import random
from trigger import trigger
from experiment_parameter import MIexperiment_components

def continuous_task(win, components, baseline, fmin, fmax, pid, day):

	condition_fname = 'result/' + pid + '__continuous_training.csv'
	
	betaIn = BetaInlet()

	data_buffer = deque([], maxlen=components.N)	#ストリーミングデータ

	#data_bufferの初期化
	while len(data_buffer) < betaIn.sampling_rate():	
		sample, timestamp = betaIn.update()
		if len(sample) != 0:
			ROI = components.channels['C4'] if components.df.iloc[[0]].hand.item() == 'left' else components.channels['C3']
			data_buffer.extend(sample.T[ROI])
	
	
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	clock = core.Clock()

	RT = []
	for blocks in range(components.blockNum):
		components.df['block'] = blocks

		eeg_fname = 'result/' + pid + '_continuous_eeg_' + day + '_b' + str(blocks) + '.csv'
		ERSP_fname = 'result/' + pid + '_FB_ERSP_' + day + '_b' + str(blocks) + '.csv'
		
		if os.path.exists(eeg_fname):
			os.remove(eeg_fname)
		if os.path.exists(ERSP_fname):
			os.remove(ERSP_fname)

		for i,row in components.df.iterrows():		
			if row['hand'] == 'left':
				trigger.SendTrigger('relax_left_b' + str(blocks+1))
				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				core.wait(components.relax_duration)

				components.cue.setText('Left')
				components.cue.draw()
				win.flip()
				core.wait(0.5)
				trigger.SendTrigger('task_left_b' + str(blocks+1))
				components.fixation.draw()
				win.flip()

				ch = components.channels['C4']
				base = baseline[0]

			else:
				trigger.SendTrigger('relax_right_b' + str(blocks+1))
				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				core.wait(components.relax_duration)

				components.cue.setText('Right')
				components.cue.draw()
				win.flip()
				core.wait(0.5)
				trigger.SendTrigger('task_right_b' + str(blocks+1))
				components.fixation.draw()
				win.flip()

				ch = components.channels['C3']
				base = baseline[1]

			t_start = clock.getTime()
			t_duration = clock.getTime() - t_start
			ERSP_List = []
			firstFlag = True
			waiting_key = True

			while waiting_key:
				sample, timestamp = betaIn.update()
				data_buffer.extend(sample.T[ch])
				display_buffer = detrend(data_buffer)
				psd, freqs = psd_array_multitaper(display_buffer, betaIn.sampling_rate(), fmin=fmin, fmax=fmax)
				ERSP = 100 * (np.average(psd) - base) / base
				if any(display_buffer > 50):
					if firstFlag:
						ERSP = 0
						firstFlag = False
					else:
						ERSP = pre_data
				ERSP_List.append(ERSP)
				circle_radius = 5*ERSP + 300
				components.Circle.setRadius(circle_radius)
				components.Circle.draw()
				components.fixation.draw()
				win.flip()

				t_duration = clock.getTime() - t_start
				if 'return' in event.getKeys(keyList=['return']):
					RT.append(t_duration)
					waiting_key = False

				pre_data = ERSP

				with open(eeg_fname, 'a') as f:
					writer = csv.writer(f, lineterminator='\n')
					writer.writerow(display_buffer)

			win.flip()
			core.wait(components.FB_duration + random.choice(components.wait_time_list))
		
			with open(ERSP_fname, 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(ERSP_List) 

			with open(eeg_fname, 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow('\n')

		components.rest(win, blocks+2)

	components.df['RT'] = RT
	components.df.insert(0, 'day', day)
	components.df.insert(0, 'condition', 'continuous')
	components.df.insert(0, 'pid', pid)
	if day == 'Day1':
		components.df.to_csv(condition_fname)
	else:
		train_df = pd.read_csv(condition_fname, index_col=0)
		pd.concat([train_df, components.df]).to_csv(condition_fname)
		
	trigger.SendTrigger('training_finish')
	components.msg.setText('Finish')
	components.msg.draw()
	win.flip()
	core.wait(1)

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	continuous_task(win, components, [500, 500], fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2])
