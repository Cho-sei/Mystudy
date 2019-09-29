"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream, resolve_byprop,\
 	proc_clocksync, proc_dejitter, proc_monotonize
from psychopy import core
from collections import deque
import numpy as np
import pandas as pd
import threading
import serial
import itertools
from scipy.signal import detrend

import csv
import time
from tqdm import tqdm

channels =  {
	'F7':0, 'Fp1':1, 'Fp2':2, 'F8':3, 'F3':4, 'Fz':5, 'F4':6, 'C3':7,
	'Cz':8, 'P8':9, 'P7':10, 'Pz':11, 'P4':12, 'T3':13, 'P3':14, 'O1':15,
	'O2':16, 'C4':17, 'T4':18, 'A2':19, 'ACC20':20, 'ACC21':21, 'ACC22':22,
	'Packet Counter':23, 'TRIGGER':24
	}

#DataFrame
conditions = list(itertools.product(
	range(2),
	('left', 'right'),
))

df = pd.DataFrame(
	conditions, columns=('block', 'hand'))

#parameter
eC3 = channels['C3']	#見たい電極
eC4 = channels['C4']	#見たい電極
eCz = channels['Cz']	#見たい電極
N = 1024
task_duration = 4			#秒
blockNum = 2
rest_duration = 2
sampling_rate = 500

#データ取得と更新
class BetaInlet(object):
	def __init__(self):
		streams = resolve_byprop("type", "EEG")

		# create a new inlet to read from the stream
		proc_flags = proc_clocksync | proc_dejitter | proc_monotonize
		self.inlet = StreamInlet(streams[0], processing_flags=proc_flags)

	def update(self):
		max_samps = 3276*2
		data = np.nan * np.ones((max_samps, 25), dtype=np.float32)
		_, timestamps = self.inlet.pull_chunk(max_samples=max_samps, dest_obj=data)
		data = data[:len(timestamps), :]
		return data, np.asarray(timestamps)

	def sampling_rate(self):
		return self.inlet.info().nominal_srate()

	def DataAquisition(self, electrode):
		data_buffer = []
		self.update()

		clock = core.Clock()
		t_start = clock.getTime()
		t_duration = clock.getTime() - t_start

		while t_duration < task_duration:	
			sample, timestamp = self.update()
			if len(sample) != 0:
				data_buffer.extend(sample.T[electrode])
			t_duration = clock.getTime() - t_start
		
		return data_buffer

if __name__ == '__main__':
	betaIn = BetaInlet()

	relax_data = []

	ser = serial.Serial('COM6', 57600)
	ser.write(b'\x00')

	for i in tqdm(range(100)):
		ser.write(b'\x30')
		relax_data = betaIn.DataAquisition(eC4)
		ser.write(b'\x00')

		time.sleep(2)

		with open('0731_nfbtest_100_3.csv', 'a') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(relax_data)