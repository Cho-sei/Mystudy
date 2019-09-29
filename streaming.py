from pylsl import StreamInlet, resolve_stream, resolve_byprop,\
 	proc_clocksync, proc_dejitter, proc_monotonize
import numpy as np
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper
import time

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
		data_buffer = []
		self.update()

		t_start = time.perf_counter()
		t_duration = time.perf_counter() - t_start

		while t_duration < duration:	
			sample, timestamp = self.update()
			if len(sample) != 0:
				data_buffer.extend(sample.T[electrode])
			t_duration = time.perf_counter() - t_start

		detrend_buffer = detrend(data_buffer)
		psd, freqs = psd_array_multitaper(detrend_buffer, self.sampling_rate(), fmin=fmin, fmax=fmax)

		return np.average(psd)