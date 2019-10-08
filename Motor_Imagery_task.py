from psychopy import visual,core,event
import itertools
import pandas as pd
import serial
import numpy as np
import winsound
from trigger import trigger
from experiment_parameter import MIexperiment_components

def MI_task(win, components, timing):
	#DataFrame
	conditions = list(itertools.product(
		range(components.MItask_trial),
		('left', 'right'),
	))
	df = pd.DataFrame(
	conditions, columns=('block', 'hand'))
	df = df.sample(frac=1)
	df.sort_values('block', inplace=True)
	df.reset_index(drop=True, inplace=True)

	clock = core.Clock()

	#display stimulus
	components.msg.setText('Start')
	components.msg.draw()
	win.flip()

	core.wait(components.ready_duration)

	RT = []
	for i, row in df.iterrows():

		if row['hand'] == 'left':

			trigger.SendTrigger('Mitest_pre_relaxleft') if timing == 'pre' else trigger.SendTrigger('Mitest_post_relaxleft')
			components.msg.setText('Relax')
			components.msg.draw()
			win.flip()

			core.wait(components.relax_duration)
			
			components.cue.setText('Left')
			components.cue.draw()
			win.flip()
			core.wait(components.cue_duration)
			trigger.SendTrigger('Mitest_pre_taskleft') if timing == 'pre' else trigger.SendTrigger('Mitest_post_taskleft')
			components.fixation.draw()
			win.flip()

		else:

			trigger.SendTrigger('Mitest_pre_relaxright') if timing == 'pre' else trigger.SendTrigger('Mitest_post_relaxright')
			components.msg.setText('Relax')
			components.msg.draw()
			win.flip()

			core.wait(components.relax_duration)
			
			components.cue.setText('Right')
			components.cue.draw()
			win.flip()
			core.wait(components.cue_duration)
			trigger.SendTrigger('Mitest_pre_taskright') if timing == 'pre' else trigger.SendTrigger('Mitest_post_taskright')
			components.fixation.draw()
			win.flip()

		t_start = clock.getTime()
		key = event.waitKeys(keyList=['return'])
		RT.append(clock.getTime() - t_start)	

	components.msg.setText('Finish')
	components.msg.draw()
	win.flip()
	core.wait(1)

	df['RT'] = RT
	df['timing'] = timing

	return df[['timing', 'block', 'hand', 'RT']]

if __name__ == '__main__':
	event.globalKeys.add(key='escape', func=core.quit)

	win = visual.Window(units='pix', fullscr=True, allowGUI=False)
	components = MIexperiment_components(win)

	MI_result = MI_task(win, components, 'pre')
	MI_result[['timing', 'block', 'hand', 'RT']].to_csv('result/test_MItask.csv')

	day = 'Day1'

	MI_result_post = MI_task(win, components, day)
	MI_df = pd.read_csv('result/test_MItask.csv', index_col=0)
	pd.concat([MI_df, MI_result_post]).to_csv('result/test_MItask.csv')

