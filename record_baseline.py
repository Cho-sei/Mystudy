from psychopy import core, visual, event, sound
from streaming import BetaInlet
import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd
from instruction import instruction
from experiment_parameter import MIexperiment_components
from trigger import trigger

def baseline(win, components, instruction, fmin, fmax, pid, day):
    betaIn = BetaInlet()

    noisy = True
    while noisy:
        components.msg.setText('Start')
        components.msg.draw()
        win.flip()

        core.wait(components.ready_duration)

        trigger.SendTrigger('baseline')    
        components.fixation.draw()
        win.flip()

        baselineLeft = []
        baselineRight = []
   
        for i in range(components.baseline_duration):
            baselineLeft.append(betaIn.DataAquisition(electrode=17, duration=1, fmin=fmin, fmax=fmax))
            baselineRight.append(betaIn.DataAquisition(electrode=7, duration=1, fmin=fmin, fmax=fmax))

        basedf = pd.DataFrame({'Left':baselineLeft, 'right':baselineRight})
        art_prob = basedf.count() / len(basedf)
        if all(art_prob > 0.7):
            noisy = False
            instruction.PresentText(text=u'安静時脳波の測定', sound='repeat_resting')

    components.msg.setText('Finish')
    components.msg.draw()
    win.flip()

    basedf.to_csv('result/' + pid + '_baseline_' + day + '.csv')

    return basedf.mean()

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)
    
    win = visual.Window(
        size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)
    
    print(baseline(win, components, instruction, fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2]))