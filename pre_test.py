from psychopy import core, visual, event, sound
import numpy as np
import sys
import pandas as pd
import KVIQ
import flandars
from experiment_parameter import MIexperiment_components
from instruction import instruction
from mental_rotation import hand_lateralization_task
from performance_test import performance_test


pid = sys.argv[1]

p_info = pd.read_csv('participants_data.csv')
condition = p_info[p_info['pid'] == pid]['condition'].item()

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)
instruction = instruction(win, components)

#--experiment start------------------------------------------------------

components.msg.setText('wait')
components.msg.draw()
win.flip()

event.waitKeys(keyList=['space'])

instruction.introduction('Day1')

#flandars handed test
instruction.inst_flandars()
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
handedDf.insert(0, 'pid', pid)
handedDf.to_csv('result/' + pid + '_FlandarsTest.csv')
win.setMouseVisible(False)

#performance test
instruction.inst_PT('pre')
PT_result = performance_test(win, components, instruction, 'pre', handed)
instruction.PresentText(text='Finish', sound='otsukaresama')
PT_result.insert(0, 'condition', condition)
PT_result.insert(0, 'pid', pid)
PT_result.to_csv('result/' + pid + '_PT.csv')

event.waitKeys(keyList=['space'])

#KVIQ
instruction.inst_KVIQ()
KVIQ_pre_result = KVIQ.KVIQ_proc(win, handed, 'pre')
instruction.PresentText(text='Finish', sound='otsukaresama')
KVIQ_pre_result.insert(0, 'condition', condition)
KVIQ_pre_result.insert(0, 'pid', pid)
KVIQ_pre_result.to_csv('result/' + pid + '_KVIQ.csv')
win.setMouseVisible(False)

#MR task
instruction.inst_MR('pre')
MR_pre_result = hand_lateralization_task(win, components, 'pre')
instruction.PresentText(text='Finish', sound='otsukaresama')
MR_pre_result.insert(0, 'condition', condition)
MR_pre_result.insert(0, 'pid', pid)
MR_pre_result.to_csv('result/' + pid + '_MR.csv')

#rest
instruction.PresentText(text=u'休憩', sound='into_rest')
event.waitKeys(keyList=['space'])

