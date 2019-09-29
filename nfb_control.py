from psychopy import visual,core,event
import itertools
import pandas as pd
import serial
import numpy as np
import winsound
import sys
import os
import random
from trigger import trigger
from experiment_parameter import MIexperiment_components

def control_task(win, components, pid, day):
	condition_fname = 'result/' + pid + '_control_condition_' + day + '.csv'
	if os.path.exists(condition_fname):
		os.remove(condition_fname)

	#define dummy
	if day == 'Day1':
		dummy = components.dummyList[0]
	elif day == 'Day2':
		dummy = components.dummyList[1]
	else:
		dummy = components.dummyList[2]

	#display stimulus
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	for blocks in range(components.blockNum):

		components.df['block'] = blocks

		for i, row in components.df.iterrows():

			if row['hand'] == 'left':

				trigger.SendTrigger('relax_left_b' + str(blocks+1))
				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				core.wait(components.relax_duration)
				
				components.cue.setText('Left')
				components.cue.draw()
				win.flip()
				core.wait(0.5)
				trigger.SendTrigger('task_left_b' + str(blocks+1))
				components.fixation.draw()
				win.flip()

			else:

				trigger.SendTrigger('relax_right_b' + str(blocks+1))
				components.msg.setText('Relax')
				components.msg.draw()
				win.flip()

				core.wait(components.relax_duration)
				
				components.cue.setText('Right')
				components.cue.draw()
				win.flip()
				core.wait(0.5)
				trigger.SendTrigger('task_right_b' + str(blocks+1))
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

			win.flip()
			core.wait(components.FB_duration + random.choice(components.wait_time_list))

		if blocks == 0:
			components.df.to_csv(condition_fname, mode='a')
		else:
			components.df.to_csv(condition_fname, mode='a', header=False)

		if blocks < components.blockNum - 1:
			components.rest(win)

	trigger.SendTrigger('training_finish')
	components.msg.setText('Finish')
	components.msg.draw()
	win.flip()
	core.wait(1)

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	control_task(win, components, pid=sys.argv[1], day=sys.argv[2])

