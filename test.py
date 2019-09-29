from psychopy import core, visual, event
from instruction import instruction
from experiment_parameter import MIexperiment_components
from streaming import BetaInlet
import time
from scipy.signal import detrend
import csv
import random

win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)

for i in range(5):
	components.msg.setText(random.choice(components.wait_time_list))
	components.msg.draw()
	win.flip()

	core.wait(1)