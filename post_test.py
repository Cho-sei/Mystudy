from psychopy import core, visual, event, sound
import numpy as np
import sys
import pandas as pd
import KVIQ
import flandars
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction
from mental_rotation import hand_lateralization_task
from performance_test import performance_test


pid = sys.argv[1]

p_info = pd.read_csv('participants_data.csv')
lateral = p_info[p_info['pid'] == pid]['lateral'].item()
hand = p_info[p_info['pid'] == pid]['hand'].item()

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)
instruction = instruction(win, components)

def questionnaire():
    instruction.inst_questionnaire()
    answers = attribute_question(win, components)
    ques_df = pd.DataFrame(columns=answers.index)
    ques_df = ques_df.append(answers, ignore_index=True)
    ques_df.insert(0, 'timing', 'post')
    ques_df.insert(0, 'lateral', lateral)
    ques_df.insert(0, 'hand', hand)
    ques_df.insert(0, 'pid', pid)
    ques_df.to_csv('result/' + pid + '_post_questionnaire.csv')

def PT():
    instruction.inst_PT()
    PT_result_post = performance_test(win, components, instruction, 'post', handed)
    instruction.PresentText(text='Finish', sound='otsukaresama')
    PT_df = pd.read_csv('result/' + pid + '_PT.csv', index_col=0)
    PT_result_post.insert(0, 'lateral', lateral)
    PT_result_post.insert(0, 'pid', pid)
    pd.concat([PT_df, PT_result_post]).to_csv('result/' + pid + '_PT.csv')

def KVIQ_test():
    instruction.inst_KVIQ()
    KVIQ_post_result = KVIQ.KVIQ_proc(win, handed, 'post')
    instruction.PresentText(text='Finish', sound='otsukaresama')
    KVIQ_df = pd.read_csv('result/' + pid + '_KVIQ.csv', index_col=0)
    KVIQ_post_result.insert(0, 'lateral', lateral)
    KVIQ_post_result.insert(0, 'pid', pid)
    pd.concat([KVIQ_df, KVIQ_post_result]).to_csv('result/' + pid + '_KVIQ.csv')

def MR():
    instruction.inst_MR()
    MR_post_result = hand_lateralization_task(win, components, 'post')
    instruction.PresentText(text='Finish', sound='otsukaresama')
    MR_df = pd.read_csv('result/' + pid + '_MR.csv', index_col=0)
    MR_post_result.insert(0, 'lateral', lateral)
    MR_post_result.insert(0, 'pid', pid)
    pd.concat([MR_df, MR_post_result]).to_csv('result/' + pid + '_MR.csv')

def ex_finish():
    instruction.inst_finish('Day3')

if __name__ == '__main__':

    components.msg.setText('wait')
    components.msg.draw()
    win.flip()

    event.waitKeys(keyList=['space'])

    questionnaire()

    #KVIQ_test()
    #MR()
    ex_finish()

    event.waitKeys(keyList=['space'])