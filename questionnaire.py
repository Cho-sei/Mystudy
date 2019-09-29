import KVIQ_inst
import KVIQ
import flandars
from psychopy import core, visual, event
import pandas as pd
import sys

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(
    size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)

#flandars handed test
handedDf = flandars.flandars_proc(win)
if handedDf['response'].sum() < -4:
    handed = 'left'
elif handedDf['response'].sum() > 4:
    handed = 'right'
else:
    handed = 'both'
handedDf.to_csv(sys.argv[1] + '_FlandarsTest.csv')

#instruction
KVIQ_inst.instruction(win)

#KVIQ
result = KVIQ.KVIQ_proc(win, handed)
result.to_csv(sys.argv[1] + '_KVIQ.csv')