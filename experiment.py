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

#--experiment start------------------------------------------------------

trigger.SendTrigger('start')

#MItest
if day == 'Day1':
	#inst_MI
	instruction.inst_MItest('pre')
else:
	instruction.introduction(day)

#MItask
instruction.inst_MItest()
trigger.SendTrigger('Mitest_pre')
MI_result = Motor_Imagery_task.MI_task(win, components, 'pre')
instruction.PresentText(text='Finish', sound='otsukaresama')
MI_result.insert(0, 'day', day)
MI_result.insert(0, 'condition', condition)
MI_result.insert(0, 'pid', pid)
MI_result.to_csv('result/' + pid + '_MItask.csv')

#inst_training
if day == 'Day1':
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
MI_result_post = Motor_Imagery_task.MI_task(win, components, 'post')
instruction.PresentText(text='Finish', sound='otsukaresama')
MI_df = pd.read_csv('result/' + pid + '_MItask.csv', index_col=0)
MI_result.insert(0, 'day', day)
MI_result_post.insert(0, 'condition', condition)
MI_result_post.insert(0, 'pid', pid)
pd.concat([MI_df, MI_result_post]).to_csv('result/' + pid + '_MItask.csv')

