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

			#if 'return' in event.getKeys(keyList=['return']):
				
			core.wait(1)
			"""
			if t_duration%(components.task_duration/len(dummy)) < 0.02:
				if (t_duration - pre_time) > 0.05:
					i += 1
					pre_time = t_duration
			"""
		detrend_buffer = detrend(data_buffer)
		
		return detrend_buffer
	

def discrete_task(win, components, baseline, fmin, fmax, pid, day):
	discrete_betaIn = discrete_DataAquisition()

	eeg_fname = 'result/' + pid + '_discrete_eeg_' + day + '.csv'
	condition_fname = 'result/' + pid + '_discrete_condition_' + day + '.csv'

	if os.path.exists(eeg_fname):
		os.remove(eeg_fname)
	if os.path.exists(condition_fname):
		os.remove(condition_fname)

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

				task_data = discrete_betaIn.DataAquisition4discrete(components.channels['C4'], win, components, dummy[blocks][i])
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

				task_data = discrete_betaIn.DataAquisition4discrete(components.channels['C3'], win, components, dummy[blocks][i])
				base = baseline[1]
			
			min_erd = float('inf')
			for steps in range(0, len(task_data)-500, 125):
				task_psd, _ = psd_array_multitaper(task_data[steps:steps+int(discrete_betaIn.sampling_rate())], discrete_betaIn.sampling_rate(), fmin=fmin, fmax=fmax)
				if min_erd > np.average(task_psd):
					min_erd = np.average(task_psd)
					final_step = steps
			steps_list.append(final_step)
			
			ERD = 100 * (min_erd - base) / base
			ERD_list.append(ERD)
			if ERD < -10:
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

		components.df['ERD'] = ERD_list
		components.df['steps'] = steps_list
		if blocks == 0:
			components.df.to_csv(condition_fname, mode='a')
		else:
			components.df.to_csv(condition_fname, mode='a', header=False)

		components.rest(win, blocks+2)

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

	discrete_task(win, components, baseline=[500, 500], fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2])