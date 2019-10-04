from psychopy import core, visual, event, sound
from streaming import BetaInlet
import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd
from instruction import instruction
from experiment_parameter import MIexperiment_components
from trigger import trigger
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper

def baseline(win, components, instruction, fmin, fmax, pid, day):
    betaIn = BetaInlet()

    baseline = pd.DataFrame(columns=['counter', 'C4', 'C3'])
    counter = 0

    while True:
        counter += 1

        components.msg.setText('Start')
        components.msg.draw()
        win.flip()

        core.wait(components.ready_duration)

        trigger.SendTrigger('baseline')    
        components.fixation.draw()
        win.flip()
   
        for i in range(components.baseline_duration):
            data = betaIn.DataAquisition(electrode=['Fp1', 'C4', 'C3'], duration=1)
            
            if any(data['Fp1'] > components.artifact_th):
                psdList = [None] * 2
            else:
                psdList = [np.average(psd_array_multitaper(data[ch], betaIn.sampling_rate(), fmin=fmin, fmax=fmax)[0]) for ch in ['C4', 'C3']]
            baseline = baseline.append(pd.Series([counter]+psdList, index=baseline.columns), ignore_index=True)
        baseline.to_csv('result/baseline_' + day + '.csv')
        art_prob = baseline[baseline.counter == counter].count() / len(baseline[baseline.counter == counter])
        if all(art_prob > 0.5):
            break
        instruction.PresentText(text=u'安静時脳波の測定', sound='repeat_resting')

    components.msg.setText('Finish')
    components.msg.draw()
    win.flip()

    baseline.to_csv('result/' + pid + '_baseline_' + day + '.csv')

    return baseline.mean()

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)
    
    win = visual.Window(
        size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)
    
    print(baseline(win, components, instruction, fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2]))