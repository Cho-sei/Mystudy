from psychopy import core, visual, event, sound
import numpy as np
import record_baseline
import nfb_control
import nfb_discrete
import nfb_continuous
import Motor_Imagery_task
import sys
from trigger import trigger
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction

pid = sys.argv[1]
day = sys.argv[2]

p_info = pd.read_csv('participants_data.csv')
condition = p_info[p_info['pid'] == pid]['condition'].item()

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)
instruction = instruction(win, components)

def inst():
	trigger.SendTrigger('start')
	if day == 'Day1':
		instruction.inst_train_proc()
		instruction.inst_MItest('pre')
	else:
		instruction.introduction(day)

def MItask(timing):
	instruction.inst_MItest()
	trigger.SendTrigger('Mitest_' + timing)
	MI_result = Motor_Imagery_task.MI_task(win, components, timing)
	instruction.PresentText(text='Finish', sound='otsukaresama')
	MI_result.insert(0, 'day', day)
	MI_result.insert(0, 'condition', condition)
	MI_result.insert(0, 'pid', pid)
	if (day == 'Day1') & (timing == 'pre'):
		MI_result.to_csv('result/' + pid + '_MItask.csv')
	else:
		MI_df = pd.read_csv('result/' + pid + '_MItask.csv', index_col=0)
		pd.concat([MI_df, MI_result]).to_csv('result/' + pid + '_MItask.csv')

def inst_train():
	if day == 'Day1':
		instruction.inst_training(condition)

def record_resting():
	instruction.inst_resting()
	baseline = record_baseline.baseline(win, components, instruction, fmin=8, fmax=13, pid=pid, day=day)
	instruction.PresentText(text='Finish', sound='otsukaresama')
	return baseline

def training(baseline):
	instruction.inst_training()
	trigger.SendTrigger('training_start')
	if condition == 'control':
		nfb_control.control_task(win, components, pid=pid, day=day)
	elif condition == 'discrete':
		nfb_discrete.discrete_task(win, components, baseline, fmin=8, fmax=13, pid=pid, day=day)
	else:
		nfb_continuous.continuous_task(win, components, baseline, fmin=8, fmax=13, pid=pid, day=day)
	instruction.PresentText(text='Finish', sound='otsukaresama')

def finish():
	if day != 'Day3':
		instruction.inst_finish(day)
	else:
		instruction.PresentText(text='Finish', sound='otsukaresama')

if __name__ == '__main__':

	components.msg.setText('wait')
	components.msg.draw()
	win.flip()

	event.waitKeys(keyList=['space'])

	inst()
	MItask('pre')
	inst_train()
	baseline = record_resting()
	#baseline = [500, 500]
	training(baseline)
	MItask('post')
	finish()


	event.waitKeys(keyList=['space'])