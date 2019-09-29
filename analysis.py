import mne
from mne.time_frequency import tfr_morlet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

blocks = 5
trials = 10

freqs = np.arange(8, 13, 0.1)
n_cycles = freqs

def calc_power(data):
    epochdata = [mne.EpochsArray(data[i], info=epochs.info) for i in range(blocks)]
    return [tfr_morlet(epochdata[i], n_cycles=n_cycles, freqs=freqs, decim=3, return_itc=False) for i in range(blocks)]

def ERD_list(power, electrode):
    return [np.average(power[i].data[power[i].ch_names.index(electrode),:,:]) for i in range(blocks)]

raw = mne.io.read_raw_brainvision('0713_contest.vhdr')
events = mne.find_events(raw, stim_channel='TRIGGER')
event_dict = {'relax':256, 'left':4096, 'right':8192}

raw.load_data()
raw.filter(l_freq=1, h_freq=50)
raw.notch_filter(freqs=60)

tmin, tmax = -0.5, 4.0
epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=tmin, tmax=tmax)

montage = mne.channels.read_montage(kind='standard_1020', ch_names=raw.ch_names)
raw.set_montage(montage=montage, set_dig=True, verbose=None)

Left = epochs['left']
Right = epochs['right']
Relax = epochs['relax']
Left_blockdata = [Left.get_data()[i:i+trials] for i in range(0,trials*blocks,trials)]
Right_blockdata = [Right.get_data()[i:i+trials] for i in range(0,trials*blocks,trials)]
Relax_blockdata = [Relax.get_data()[i:i+trials*2] for i in range(0,trials*blocks*2,trials*2)]

Left_power = calc_power(Left_blockdata)
Right_power = calc_power(Right_blockdata)
Relax_power = calc_power(Relax_blockdata)

Xaxis = np.arange(1,6)
plt.ylim(-5e-10, 2e-10)
plt.subplots_adjust(wspace=0.4, hspace=0.6)
for i, (hand, ch) in enumerate(product(['Left', 'Right'], ['C3', 'C4'])):
    plt.subplot(2, 2, i+1)
    plt.title(hand + ch)
    MI_power = Left_power if hand == 'Left' else Right_power
    MI_ERD = ERD_list(MI_power, ch)
    Relax_ERD = ERD_list(Relax_power, ch)
    ERSP = [100 * (MI_ERD[i] - Relax_ERD[i]) / Relax_ERD[i] for i in range(blocks)]
    plt.bar(Xaxis, ERSP, color='blue', align='center')
    plt.savefig('0713_contest.png')