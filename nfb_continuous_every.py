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
from record_baseline_every import baseline as bsl
from fatigue import fatigue_VAS
import csv
import sys
import os
import random
from trigger import trigger
from experiment_parameter import MIexperiment_components
from scipy import signal
 
#バターワースフィルタ（ローパス）
def lowpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

def continuous_task(win, components, lateral, hand, fmin, fmax, pid, day):

	condition_fname = 'result/' + pid + '_continuous_training_' + day + '.csv'
	fatigue_fname = 'result/' + pid + '_block_questionnaire_' + day + '.csv'
	
	betaIn = BetaInlet()

	data_buffer = deque([], maxlen=components.N)	#ストリーミングデータ
	data_buffer_blink = deque([], maxlen=components.N)	#ストリーミングデータ
	summary = pd.DataFrame()
	pre_baseline = pd.DataFrame({'C4':[500], 'C3':[500]})

	if hand == 'right':
		el = 'C3'
	else:
		el = 'C4'

	fatigue_res = []
	concentrate_res = []
	difficulty_res = []
	prediction_res = []
	sleepiness_res = []
	visualScale = []
	kinethesticScale = []

	#data_bufferの初期化
	while len(data_buffer) < components.N:	
		sample, timestamp = betaIn.update()
		if len(sample) != 0:
			ROI = components.channels[el]
			data_buffer.extend(sample.T[ROI])
	
	
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	clock = core.Clock()

	for blocks in range(components.blockNum):
		components.df['block'] = blocks

		eeg_fname = 'result/' + pid + '_continuous_eeg_' + day + '_b' + str(blocks) + '.csv'
		ERSP_fname = 'result/' + pid + '_FB_ERSP_' + day + '_b' + str(blocks) + '.csv'
		
		if os.path.exists(eeg_fname):
			os.remove(eeg_fname)
		if os.path.exists(ERSP_fname):
			os.remove(ERSP_fname)

		RT = []
		for i,row in components.df.iterrows():		
			trigger.SendTrigger('relax_b' + str(blocks+1))
			components.msg.setText('Relax')
			components.msg.draw()
			win.flip()

			baseline = bsl(win, components, fmin, fmax, pid, day, blocks, i, pre_baseline)

			trigger.SendTrigger('task_b' + str(blocks+1))
			components.fixation.draw()
			win.flip()

			ch = components.channels[el]
			base = baseline[el]

			pre_baseline = baseline

			t_start = clock.getTime()
			t_duration = clock.getTime() - t_start
			ERSP_List = []
			firstFlag = True
			waiting_key = True

			while waiting_key:
				sample, timestamp = betaIn.update()
				data_buffer.extend(sample.T[ch])
				data_buffer_blink.extend(sample.T[1])
				display_buffer = detrend(data_buffer)
				display_buffer_blink = detrend(data_buffer_blink)
				display_buffer = lowpass(display_buffer, betaIn.sampling_rate(), fp=40, fs=50, gpass=3, gstop=40)
				display_buffer_blink = lowpass(display_buffer_blink, betaIn.sampling_rate(), fp=40, fs=50, gpass=3, gstop=40)
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

		fatigue_return = fatigue_VAS(win, components)
		fatigue_res.append(fatigue_return['fatigue'])
		concentrate_res.append(fatigue_return['concentrate'])
		difficulty_res.append(fatigue_return['difficulty'])
		prediction_res.append(fatigue_return['prediction'])
		sleepiness_res.append(fatigue_return['sleepiness'])
		visualScale.append(fatigue_return['VisualScale'])
		kinethesticScale.append(fatigue_return['KinethesticScale'])
		components.rest(win, blocks+2)

		print(fatigue_return)

		components.df['RT'] = RT
		summary = pd.concat([summary, components.df])

	fatigue_df = pd.DataFrame({'fatigue':fatigue_res, 
							   'concentrate':concentrate_res,
							   'difficulty':difficulty_res,
							   'prediction':prediction_res, 
							   'sleepiness':sleepiness_res,
							   'visualScale':visualScale,
							   'kinethesticScale':kinethesticScale})
	fatigue_df.insert(0, 'block', range(components.blockNum))
	fatigue_df.insert(0, 'day', day)
	fatigue_df.insert(0, 'lateral', lateral)
	fatigue_df.insert(0, 'hand', hand)
	fatigue_df.insert(0, 'pid', pid)

	summary.insert(0, 'day', day)
	summary.insert(0, 'lateral', lateral)
	summary.insert(0, 'hand', hand)
	summary.insert(0, 'pid', pid)
	
	summary.to_csv(condition_fname)
	fatigue_df.to_csv(fatigue_fname)
		
	core.wait(1)

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	continuous_task(win, components, 'right', 'right', fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2])
