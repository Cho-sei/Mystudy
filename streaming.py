from pylsl import StreamInlet, resolve_stream, resolve_byprop,\
 	proc_clocksync, proc_dejitter, proc_monotonize
import numpy as np
import pandas as pd
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper
import time

channels =  {'F7':0, 'Fp1':1, 'Fp2':2, 'F8':3, 'F3':4, 'Fz':5, 'F4':6, 'C3':7,
			'Cz':8, 'P8':9, 'P7':10, 'Pz':11, 'P4':12, 'T3':13, 'P3':14, 'O1':15,
			'O2':16, 'C4':17, 'T4':18, 'A2':19, 'ACC20':20, 'ACC21':21, 'ACC22':22,
			'Packet Counter':23, 'TRIGGER':24
			}

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

	def DataAquisition(self, electrode, duration, fmin, fmax):
		data = pd.DataFrame(columns=electrode)
		psdList = []
		self.update()

		t_start = time.perf_counter()
		t_duration = time.perf_counter() - t_start

		while t_duration < duration:
			sample, timestamp = self.update()
			
			if len(sample) != 0:
				data = data.append(pd.DataFrame(sample.T[[channels[ch] for ch in electrode]].T, columns=data.columns))
				
			t_duration = time.perf_counter() - t_start

		for ch in data:
			detrend_buffer = detrend(data[ch])
			if any(detrend_buffer > 50):
				psdList.append(None)
			else:
				psdList.append(np.average(psd_array_multitaper(detrend_buffer, self.sampling_rate(), fmin=fmin, fmax=fmax)[0]))

		return psdList
