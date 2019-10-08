"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream, resolve_byprop,\
 	proc_clocksync, proc_dejitter, proc_monotonize
from psychopy import visual, event, core
from collections import deque
import numpy as np
import pandas as pd
import threading
import serial
import itertools
from mne.time_frequency.multitaper import psd_array_multitaper
from scipy.signal import detrend
import csv
import os
import sys
import winsound
import random
from streaming import BetaInlet
from fatigue import fatigue_VAS
from record_baseline import baseline
from trigger import trigger
from experiment_parameter import MIexperiment_components


#データ取得と更新
class discrete_DataAquisition(BetaInlet):
	def DataAquisition4discrete(self, electrode, win, components, dummy):
		data_buffer = []
		self.update()

		clock = core.Clock()
		t_start = clock.getTime()
		t_duration = clock.getTime() - t_start

		i = 0
		pre_time = 0
		waiting_key = True
		while waiting_key:	
			sample, timestamp = self.update()
			if len(sample) != 0:
				data_buffer.extend(sample.T[electrode])
			t_duration = clock.getTime() - t_start

			components.Circle.setRadius(5*dummy[i] + 300)
			components.Circle.draw()
			components.fixation.draw()
			win.flip()

			if t_duration%0.1 < 0.02:
				if (t_duration - pre_time) > 0.05:
					i += 1
					pre_time = t_duration
			
			if i == len(dummy)-1:
				i = 0
			
			if 'return' in event.getKeys(keyList=['return']):
				RT = t_duration
				waiting_key = False
			
		detrend_buffer = detrend(data_buffer)
		
		return detrend_buffer, RT
	

def discrete_task(win, components, baseline, fmin, fmax, pid, day):
	discrete_betaIn = discrete_DataAquisition()

	eeg_fname = 'result/' + pid + '_discrete_eeg_' + day + '.csv'
	condition_fname = 'result/' + pid + '_discrete_trainig.csv'
	fatigue_fname = 'result/' + pid + '_fatigue.csv'

	if os.path.exists(eeg_fname):
		os.remove(eeg_fname)

	summary = pd.DataFrame()
	fatigue_res = []
	concentrate_res = []
	
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

		components.df['block'] = blocks

		RT_list = []
		ERD_list = []
		steps_list = []

		for i, row in components.df.iterrows():
					
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

				task_data, RT = discrete_betaIn.DataAquisition4discrete(components.channels['C4'], win, components, dummy[blocks][i])
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

				task_data, RT = discrete_betaIn.DataAquisition4discrete(components.channels['C3'], win, components, dummy[blocks][i])
				base = baseline[1]
			
			RT_list.append(RT)

			min_erd = float('inf')
			final_step = 0
			for steps in range(0, len(task_data)-500, 125):
				task_psd, _ = psd_array_multitaper(task_data[steps:steps+int(discrete_betaIn.sampling_rate())], discrete_betaIn.sampling_rate(), fmin=fmin, fmax=fmax)
				ERD = 100 * (np.average(task_psd) - base) / base
				if min_erd > ERD:
					min_erd = ERD
					final_step = steps
			steps_list.append(final_step)

			ERD_list.append(min_erd)
			if min_erd < -10:
				components.msg.setText('GOOD!')
			else:
				components.msg.setText('BAD...')

			components.msg.draw()
			win.flip()

			with open(eeg_fname, 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(task_data)

			core.wait(components.FB_duration)

			win.flip()
			
			core.wait(random.choice(components.wait_time_list))

		fatigue_return = fatigue_VAS(win, components)
		fatigue_res.append(fatigue_return[0])
		concentrate_res.append(fatigue_return[1])
		components.rest(win, blocks+2)

		components.df['ERD'] = ERD_list
		components.df['steps'] = steps_list
		components.df['RT'] = RT_list
		summary = pd.concat([summary, components.df])

	fatigue_df = pd.DataFrame({'fatigue':fatigue_res, 'concentrate':concentrate_res})
	fatigue_df.insert(0, 'block', range(components.blockNum))
	fatigue_df.insert(0, 'day', day)
	fatigue_df.insert(0, 'condition', 'discrete')
	fatigue_df.insert(0, 'pid', pid)

	summary.insert(0, 'day', day)
	summary.insert(0, 'condition', 'discrete')
	summary.insert(0, 'pid', pid)
	if day == 'Day1':
		summary.to_csv(condition_fname)
		fatigue_df.to_csv(fatigue_fname)
	else:
		if os.path.exists(fatigue_fname):
			fat_df = pd.read_csv(fatigue_fname, index_col=0)
			pd.concat([fat_df, fatigue_df]).to_csv(fatigue_fname)
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

	win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	discrete_task(win, components, baseline=[500, 500], fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2])