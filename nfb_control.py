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

		RT = []
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
			pre_time = 0
			waiting_key = True
			while waiting_key:	
				components.Circle.setRadius(5*dummy[blocks][i][j] + 300)
				components.Circle.draw()
				components.fixation.draw()
				win.flip()

				if t_duration%0.1 < 0.02:
					if (t_duration - pre_time) > 0.05:
						j += 1
						pre_time = t_duration

				if j == len(dummy[blocks][i])-1:
					j = 0
				
				t_duration = clock.getTime() - t_start
				if 'return' in event.getKeys(keyList=['return']):
					RT.append(t_duration)
					waiting_key = False

			win.flip()
			core.wait(components.FB_duration + random.choice(components.wait_time_list))

		components.df['RT'] = RT
		if blocks == 0:
			components.df.to_csv(condition_fname, mode='a')
		else:
			components.df.to_csv(condition_fname, mode='a', header=False)

		components.rest(win, blocks+2)

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

