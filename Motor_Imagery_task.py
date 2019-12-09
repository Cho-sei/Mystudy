from psychopy import visual,core,event
import itertools
import pandas as pd
import serial
import numpy as np
import winsound
from trigger import trigger
from experiment_parameter import MIexperiment_components
import random

def MI_task(win, components, timing):

	clock = core.Clock()

	#display stimulus
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	RT = []
	for i, row in components.df.iterrows():
		trigger.SendTrigger('Mitest_pre_relax') if timing == 'pre' else trigger.SendTrigger('Mitest_post_relax')
		components.msg.setText('Relax')
		components.msg.draw()
		win.flip()

		core.wait(components.relax_duration)
		
		trigger.SendTrigger('Mitest_pre_task') if timing == 'pre' else trigger.SendTrigger('Mitest_post_task')
		components.fixation.draw()
		win.flip()

		t_start = clock.getTime()
		key = event.waitKeys(keyList=['return'])
		RT.append(clock.getTime() - t_start)

		win.flip()
		core.wait(components.FB_duration + random.choice(components.wait_time_list))	

	components.msg.setText('Finish')
	components.msg.draw()
	win.flip()
	core.wait(1)

	components.df['RT'] = RT
	components.df['timing'] = timing

	return components.df[['timing', 'trial', 'RT']]

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	MI_result = MI_task(win, components, 'pre')
	MI_result[['timing', 'trial', 'RT']].to_csv('result/test_MItask.csv')

	day = 'Day1'

	MI_result_post = MI_task(win, components, day)
	MI_df = pd.read_csv('result/test_MItask.csv', index_col=0)
	pd.concat([MI_df, MI_result_post]).to_csv('result/test_MItask.csv')

