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
from mne.time_frequency.multitaper import psd_array_multitaper
import matplotlib.pyplot as plt

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
fmin, fmax = 8, 13		#見たい帯域
N = 1024
task_duration = 4			#秒
blockNum = 1
rest_duration = 2


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

def DataAquisition(electrode):
	betaIn = BetaInlet()
	#data_buffer = deque([], maxlen=N)
	data_buffer = []

	clock = core.Clock()
	t_start = clock.getTime()
	t_duration = clock.getTime() - t_start

	while t_duration < task_duration:	
		sample, timestamp = betaIn.update()
		if len(sample) != 0:
			data_buffer.extend(sample.T[electrode])
		t_duration = clock.getTime() - t_start

	detrend_buffer = detrend(data_buffer)
	psd, freqs = psd_array_multitaper(detrend_buffer, betaIn.sampling_rate(), fmin=fmin, fmax=fmax)

	print(len(detrend_buffer))

	return psd, freqs

if __name__ == '__main__':

	relax_data = []
	task_data = []

	ser = serial.Serial('COM6', 57600)

	#display stimulus
	ser.write(b'h')
	core.wait(0.1)
	ser.write(b'\x00')

	core.wait(0.1)

	for blocks in range(blockNum):

		df = df.sample(frac=1)
		df['block'] = blocks
		#df.sort_values('block', inplace=True)
		df.reset_index(drop=True, inplace=True)
		ERD_list = []
		task_list = []
		relax_list = []

		psd_data, freq = DataAquisition(eC4)

		print(freq)
		with open('discrete_eeg.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(psd_data)

		"""
		for i, row in df.iterrows():
			if row['hand'] == 'left':
				ser.write(b'\x01')
				core.wait(0.1)
				ser.write(b'\x00')

				relax_data = DataAquisition(eC4)

				ser.write(b'\x10')
				core.wait(0.1)
				ser.write(b'\x00')

				task_data = DataAquisition(eC4)
			else:
				ser.write(b'\x02')
				core.wait(0.1)
				ser.write(b'\x00')

				relax_data = DataAquisition(eC3)

				ser.write(b'\x20')
				core.wait(0.1)
				ser.write(b'\x00')

				task_data = DataAquisition(eC3)
			
			ERD = 100 * ((np.average(task_data) - np.average(relax_data)) / np.average(relax_data))
			ERD_list.append(ERD)
			task_list.append(np.average(task_data))
			relax_list.append(np.average(relax_data))
			print(np.average(task_data), np.average(relax_data), ERD)

			with open('discrete_eeg.csv', 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(task_data)
				writer.writerow(relax_data)
	
		df['task'] = task_list
		df['relax'] = relax_list
		df['ERD'] = ERD_list
		if blocks == 0:
			df.to_csv('discretetest.csv')
		else:
			df.to_csv('discretetest.csv', mode='a', header=False)

		if blocks < blockNum - 1:
			ser.write(b'\x05')
			core.wait(0.1)
			ser.write(b'\x00')
			core.wait(0.1)
		"""

	"""
	clock = core.Clock()

	t_start = clock.getTime()
	t_duration = clock.getTime() - t_start

	while t_duration < ex_duration:
		sample, timestamp = betaIn.update()
		data_buffer.extend(sample.T[ROI])
		freq, Amp = fft()
		alpha = Amp[8:13]
		circle_radius = np.average(alpha)

		t_duration = clock.getTime() - t_start

		win.flip()
	"""

