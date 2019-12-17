from psychopy import core, visual, event, sound
import numpy as np
import nfb_control
import nfb_discrete_every
import nfb_continuous_every
import Motor_Imagery_task
import sys
from trigger import trigger
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction
from fatigue import post_question, pre_train_question

pid = sys.argv[1]
day = sys.argv[2]

p_info = pd.read_csv('participants_data.csv')
lateral = p_info[p_info['pid'] == pid]['lateral'].item()
hand = p_info[p_info['pid'] == pid]['hand'].item()

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)
instruction = instruction(win, components)

def inst():
	trigger.SendTrigger('start')
	instruction.introduction(day)

def pre_question():
	if day == 'Day1':
		instruction.inst_questionnaire('pre')
	else:
		instruction.inst_questionnaire()
	answers = pre_train_question(win, components)
	ques_df = pd.DataFrame(columns=answers.index)
	ques_df = ques_df.append(answers, ignore_index=True)
	ques_df.insert(0, 'day', day)
	ques_df.insert(0, 'lateral', lateral)
	ques_df.insert(0, 'hand', hand)
	ques_df.insert(0, 'pid', pid)
	ques_df.to_csv('result/' + pid + '_pre_train_questionnaire_' + day + '.csv')

def MItask(timing):
	instruction.inst_MItest()
	trigger.SendTrigger('Mitest_' + timing)
	MI_result = Motor_Imagery_task.MI_task(win, components, timing)
	instruction.PresentText(text='Finish', sound='otsukaresama')
	MI_result.insert(0, 'day', day)
	MI_result.insert(0, 'lateral', lateral)
	MI_result.insert(0, 'hand', hand)
	MI_result.insert(0, 'pid', pid)
	if (day == 'Day1') & (timing == 'pre'):
		MI_result.to_csv('result/' + pid + '_MItask.csv')
	else:
		MI_df = pd.read_csv('result/' + pid + '_MItask.csv', index_col=0)
		pd.concat([MI_df, MI_result]).to_csv('result/' + pid + '_MItask.csv')

def training():
	instruction.inst_training()
	trigger.SendTrigger('training_start')
	nfb_continuous_every.continuous_task(win, components, lateral, hand, fmin=8, fmax=13, pid=pid, day=day)

if __name__ == '__main__':

	components.msg.setText('wait')
	components.msg.draw()
	win.flip()

	event.waitKeys(keyList=['space'])

	if day != 'Day1':
		inst()
	#pre_question()
	#MItask('pre')
	#components.rest(win, 20)
	training()
	MItask('post')

	if day == 'Day3':
		instruction.inst_questionnaire()
		answers = post_question(win, components)
		ques_df = pd.DataFrame(columns=answers.index)
		ques_df = ques_df.append(answers, ignore_index=True)
		ques_df.insert(0, 'timing', 'post')
		ques_df.insert(0, 'lateral', lateral)
		ques_df.insert(0, 'hand', hand)
		ques_df.insert(0, 'pid', pid)
		ques_df.to_csv('result/' + pid + '_post_questionnaire.csv')

		instruction.inst_finish('Day3')

	event.waitKeys(keyList=['space'])