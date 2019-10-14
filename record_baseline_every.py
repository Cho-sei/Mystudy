from psychopy import core, visual, event, sound
from streaming import BetaInlet
import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd
from instruction import instruction
from experiment_parameter import MIexperiment_components
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper

def baseline(win, components, fmin, fmax, pid, day, block, trial, pre_baseline):
    betaIn = BetaInlet()

    baseline = pd.DataFrame(columns=['C4', 'C3'])

    for i in range(components.relax_duration*2):
        data = betaIn.DataAquisition(electrode=['Fp1', 'C4', 'C3'], duration=0.5)
        
        if any(data['Fp1'] > components.artifact_th):
            psdList = [None] * 2
        else:
            psdList = [np.average(psd_array_multitaper(data[ch], betaIn.sampling_rate(), fmin=fmin, fmax=fmax)[0]) for ch in ['C4', 'C3']]
        baseline = baseline.append(pd.Series(psdList, index=baseline.columns), ignore_index=True)
    art_prob = baseline.count() / len(baseline)
    if any(art_prob == 0):
        baseline['C4'] = pre_baseline['C4']
        baseline['C3'] = pre_baseline['C3']

    baseline.insert(0, 'trial', trial)
    baseline.insert(0, 'block', block)
    baseline.insert(0, 'day', day)
    if (day == 'Day1') & (block == 0) & (trial == 0):
        baseline.to_csv('result/' + pid + '_baseline.csv')
    else:
        base_df = pd.read_csv('result/' + pid + '_baseline.csv', index_col=0)
        pd.concat([base_df, baseline]).to_csv('result/' + pid + '_baseline.csv')

    return baseline.mean()

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)
    
    win = visual.Window(
        size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)
    
    for i in range(5):
        print(baseline(win, components, fmin=8, fmax=13, pid=sys.argv[1], day=sys.argv[2], block=1, trial=i, pre_baseline=[500, 500]))