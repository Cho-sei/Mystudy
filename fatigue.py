from psychopy import core, visual, event, sound
import pandas as pd
from trigger import trigger
from experiment_parameter import MIexperiment_components
from instruction import instruction

inst_fatigue = sound.Sound('voicedata/inst_fatigue.wav')

def fatigue_VAS(win, components, instruction, pid, day, block):
    ratingScale = visual.RatingScale(
        win, high=10, precision=100, size=2.0, labels=False, pos=(0.0, -100), scale=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5,
        markerStart=50, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        ratingScale.draw()
        win.flip()
    response = ratingScale.getRating()
    return response

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)

    print(fatigue_VAS(win, components, instruction, 'test', 'test', 'test'))
	