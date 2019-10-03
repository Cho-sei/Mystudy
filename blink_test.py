from streaming import BetaInlet
from scipy.signal import detrend
import pandas as pd
import numpy

betaIn = BetaInlet()

data = betaIn.DataAquisition(electrode=['Fp1'], duration=5)
data['Fp1'] = detrend(data['Fp1'])
th = (data.max() - data.mean()) * 0.6
print(th)

while True:
	data = betaIn.DataAquisition(electrode=['Fp1'], duration=1)
	data['Fp1'] = detrend(data['Fp1'])
	
	if any(data['Fp1'] > th.item()):
		judge = 'blink' 
	else:
		judge = 'no'
	print(judge, data['Fp1'].max())