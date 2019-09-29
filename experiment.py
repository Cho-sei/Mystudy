from psychopy import core, visual, event, sound
import numpy as np
import record_baseline
import nfb_control
import nfb_discrete
import nfb_continuous
import Motor_Imagery_task
import sys
import pandas as pd
from trigger import trigger
import KVIQ
import flandars
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction
from mental_rotation import hand_lateralization_task
from performance_test import performance_test


pid = sys.argv[1]
day = sys.argv[2]

p_info = pd.read_csv('participants_data.csv')
condition = p_info[p_info['pid'] == pid]['condition'].item()

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)
instruction = instruction(win, components)

#--experiment start------------------------------------------------------

trigger.SendTrigger('start')
instruction.introduction(day)

#MItest
if day == 'Day1':
	
	#flandars handed test
	instruction.inst_flandars()
	trigger.SendTrigger('flandars')
	handedDf = flandars.flandars_proc(win)
	#handedDf = pd.read_csv('result/sha1_FlandarsTest.csv')
	instruction.PresentText(text='Finish', sound='finish_flandars')
	if handedDf['response'].sum() < -4:
	    handed = 'left'
	elif handedDf['response'].sum() > 4:
	    handed = 'right'
	else:
	    handed = 'both'
	handedDf.insert(0, 'condition', condition)
	handedDf.to_csv('result/' + pid + '_FlandarsTest.csv')
	win.setMouseVisible(False)

	#KVIQ
	instruction.inst_KVIQ()
	trigger.SendTrigger('KVIQ_pre')
	KVIQ_pre_result = KVIQ.KVIQ_proc(win, handed, 'pre')
	instruction.PresentText(text='Finish', sound='otsukaresama')
	KVIQ_pre_result.insert(0, 'condition', condition)
	KVIQ_pre_result.to_csv('result/' + pid + '_KVIQ.csv')
	win.setMouseVisible(False)

	#MR task
	instruction.inst_MR('pre')
	MR_pre_result = hand_lateralization_task(win, components, 'pre')
	instruction.PresentText(text='Finish', sound='otsukaresama')
	MR_pre_result.insert(0, 'condition', condition)
	MR_pre_result.to_csv('result/' + pid + '_MR.csv')

	#MItask
	instruction.inst_MItest('pre')
	trigger.SendTrigger('Mitest_pre')
	MI_result = Motor_Imagery_task.MI_task(win, components, 'pre')
	instruction.PresentText(text='Finish', sound='otsukaresama')
	MI_result.insert(0, 'condition', condition)
	MI_result.to_csv('result/' + pid + '_MItask.csv')

	#performance test
	instruction.inst_PT('pre')
	trigger.SendTrigger('performance_pre')
	PT_result = performance_test(win, components, 'pre', handed)
	instruction.PresentText(text='Finish', sound='otsukaresama')
	PT_result.insert(0, 'condition', condition)
	PT_result.to_csv('result/' + pid + '_PT.csv')

	#rest
	instruction.PresentText(text=u'休憩', sound='into_rest')
	event.waitKeys(keyList=['space'])

	#inst_training
	instruction.inst_training(condition)


#recording baseline
instruction.inst_resting()
baseline = record_baseline.baseline(win, components, fmin=8, fmax=13, pid=pid, day=day)
#baseline = [500, 500]
instruction.PresentText(text='Finish', sound='otsukaresama')

#into training
instruction.inst_training()
trigger.SendTrigger('training_start')
if condition == 'control':
    nfb_control.control_task(win, components, pid=pid, day=day)
elif condition == 'discrete':
    nfb_discrete.discrete_task(win, components, baseline, fmin=8, fmax=13, pid=pid, day=day)
else:
    nfb_continuous.continuous_task(win, components, baseline, fmin=8, fmax=13, pid=pid, day=day)
instruction.PresentText(text='Finish', sound='otsukaresama')

#MItest
instruction.inst_MItest()
trigger.SendTrigger('Mitest_post')
MI_result_post = Motor_Imagery_task.MI_task(win, components, day)
instruction.PresentText(text='Finish', sound='otsukaresama')
MI_df = pd.read_csv('result/' + pid + '_MItask.csv', index_col=0)
MI_result_post.insert(0, 'condition', condition)
pd.concat([MI_df, MI_result_post]).to_csv('result/' + pid + '_MItask.csv')

if day == 'Day3':
	#performance test
	instruction.inst_PT()
	trigger.SendTrigger('performance_post')
	PT_result_post = performance_test(win, components, 'post', handed)
	instruction.PresentText(text='Finish', sound='otsukaresama')
	PT_df = pd.read_csv('result/' + pid + '_PT.csv', index_col=0)
	PT_result_post.insert(0, 'condition', condition)
	pd.concat([PT_df, PT_result_post]).to_csv('result/' + pid + '_PT.csv')

	#KVIQ
	handedDf = pd.read_csv('result/' + pid + '_FlandarsTest.csv')
	if handedDf['response'].sum() < -4:
	    handed = 'left'
	elif handedDf['response'].sum() > 4:
	    handed = 'right'
	else:
	    handed = 'both'
	instruction.PresentText(text=u'運動イメージ検査', sound='KVIQ_post')
	trigger.SendTrigger('KVIQ_post')
	KVIQ_post_result = KVIQ.KVIQ_proc(win, handed, 'post')
	instruction.PresentText(text='Finish', sound='otsukaresama')
	KVIQ_df = pd.read_csv('result/' + pid + '_KVIQ.csv')
	KVIQ_post_result.insert(0, 'condition', condition)
	pd.concat([KVIQ_df, KVIQ_post_result]).to_csv('result/' + pid + '_KVIQ.csv')

	#MR task
	instruction.inst_MR()
	MR_post_result = hand_lateralization_task(win, components, 'post')
	instruction.PresentText(text='Finish', sound='otsukaresama')
	MR_df = pd.read_csv('result/' + pid + '_MR.csv', index_col=0)
	MR_post_result.insert(0, 'condition', condition)
	pd.concat([MR_df, MR_post_result]).to_csv('result/' + pid + '_MR.csv')

trigger.SendTrigger('finish')
instruction.inst_finish(day)