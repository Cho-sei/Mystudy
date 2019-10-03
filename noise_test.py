from streaming import BetaInlet
import numpy as np
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper

betaIn = BetaInlet()

fmin, fmax = 8, 13
while True:
	data = betaIn.DataAquisition(electrode=['C3', 'C4'], duration=1, fmin=fmin, fmax=fmax)
	psdList = []
	for ch in data:
		detrend_buffer = detrend(data[ch])
		if any(detrend_buffer > 50):
			psdList.append(None)
		else:
			psdList.append(np.average(psd_array_multitaper(detrend_buffer, betaIn.sampling_rate(), fmin=fmin, fmax=fmax)[0]))
	print(psdList)