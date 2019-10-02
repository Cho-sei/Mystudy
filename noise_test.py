from streaming import BetaInlet
import numpy as np

betaIn = BetaInlet()

fmin, fmax = 8, 13
while True:
	print(betaIn.DataAquisition(electrode=['C3', 'C4'], duration=1, fmin=fmin, fmax=fmax))