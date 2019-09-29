from psychopy import visual,core,event
import itertools
import pandas as pd
import serial
import numpy as np
import winsound
import sys
import os
from experiment_parameter import MIexperiment_components

def demo(win, components):

	#define dummy
	dummy = components.dummyList[0]
	
	#display stimulus
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	for blocks in range(components.blockNum):

		components.df['block'] = blocks

		for i, row in components.df.iterrows():

			if row['hand'] == 'left':

				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				core.wait(components.relax_duration)
				
				components.cue.setText('Left')
				components.cue.draw()
				win.flip()
				core.wait(0.5)
				components.fixation.draw()
				win.flip()

			else:

				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				core.wait(components.relax_duration)
				
				components.cue.setText('Right')
				components.cue.draw()
				win.flip()
				core.wait(0.5)
				components.fixation.draw()
				win.flip()

			clock = core.Clock()
			t_start = clock.getTime()
			t_duration = clock.getTime() - t_start

			j = 0
			while t_duration < components.task_duration:	
				components.Circle.setRadius(5*dummy[blocks][i][j] + 300)
				components.Circle.draw()
				components.fixation.draw()
				core.wait(components.task_duration/len(dummy[blocks][i]))
				win.flip()
				j += 1
				t_duration = clock.getTime() - t_start

		if blocks < components.blockNum - 1:
			for time in reversed(range(1, self.rest_duration+1)):
				components.msg.setText('Rest')
				components.msg.draw()
				components.countText.setText(time)
				components.countText.draw()
				win.flip()

				if time < 4:
					winsound.Beep(1000, 100)

				core.wait(1)

	components.msg.setText('Finish')
	components.msg.draw()
	win.flip()
	core.wait(1)

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	demo(win, components)

