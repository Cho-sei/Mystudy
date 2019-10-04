from streaming import BetaInlet
import numpy as np
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper

betaIn = BetaInlet()

fmin, fmax = 8, 13
while True:
	data = betaIn.DataAquisition(electrode=['Fp1', 'C3', 'C4'], duration=1)
	psdList = []
	
	if any(data['Fp1'] > 100):
		psdList = [None] * 2
	else:
		for ch in ['C3', 'C4']:
			psdList.append(np.average(psd_array_multitaper(data[ch], betaIn.sampling_rate(), fmin=fmin, fmax=fmax)[0]))
	print(psdList)