"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream, resolve_byprop,\
 	proc_clocksync, proc_dejitter, proc_monotonize
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import msvcrt
from scipy.signal import detrend
from mne.time_frequency.multitaper import psd_array_multitaper
import time

channels =  {
	'F7':0, 'Fp1':1, 'Fp2':2, 'F8':3, 'F3':4, 'Fz':5, 'F4':6, 'C3':7,
	'Cz':8, 'P8':9, 'P7':10, 'Pz':11, 'P4':12, 'T3':13, 'P3':14, 'O1':15,
	'O2':16, 'C4':17, 'T4':18, 'A2':19, 'ACC20':20, 'ACC21':21, 'ACC22':22,
	'Packet Counter':23, 'TRIGGER':24
	}
#parameter
#ROI_elec = 'O1'
#ROI = channels[ROI_elec]	#見たい電極
ROI = 7
N = 10000

#データ取得と更新
class BetaInlet(object):
    def __init__(self):
        print("looking for an EEG stream...")
        streams = resolve_byprop("type", "EEG")

        # create a new inlet to read from the stream
        proc_flags = proc_clocksync | proc_dejitter | proc_monotonize
        self.inlet = StreamInlet(streams[0], processing_flags=proc_flags)

        stream_info = self.inlet.info()
        stream_xml = stream_info.desc()
        chans_xml = stream_xml.child("channels")
        self.channel_list = []
        ch = chans_xml.child("channel")
        while ch.name() == "channel":
            self.channel_list.append(ch)
            ch = ch.next_sibling("channel")

    def update(self):
        max_samps = 3276*2
        data = np.nan * np.ones((max_samps, len(self.channel_list)), dtype=np.float32)
        _, timestamps = self.inlet.pull_chunk(max_samples=max_samps, dest_obj=data)
        data = data[:len(timestamps), :]
        return data, np.asarray(timestamps)

    def sampling_rate(self):
    	return self.inlet.info().nominal_srate()


if __name__ == '__main__':

    betaIn = BetaInlet()
    sampling_rate = betaIn.sampling_rate()

    data_buffer = deque([], maxlen=N)	#ストリーミングデータ

    #data_bufferの初期化
    while len(data_buffer) < N:	
        sample, timestamp = betaIn.update()
        if len(sample) != 0:
            data_buffer.extend(sample.T[ROI])

    m = np.average(data_buffer)

    display_buffer = detrend(data_buffer)

    #初期値グラフ表示
    x = np.arange(0, len(display_buffer), 1)
    plt.figure(figsize=(10,6))
    plt.subplot(211)
    f, = plt.plot(x, display_buffer)
    #plt.ylim(m - (m - min(display_buffer)) * 10, m + (max(display_buffer) - m) * 10)
    psd, freqs = psd_array_multitaper(display_buffer, betaIn.sampling_rate(), fmin=8, fmax=13)
    #target_band_index = np.where((freqs > fmin) & (freqs < fmax))[0]
    plt.subplot(212)
    F, = plt.plot(freqs, psd)
    #plt.xlim(0, 60)
    #plt.ylim(0, 1e14)

    #無限プロット
    while True:
        sample, timestamp = betaIn.update()
        data_buffer.extend(sample.T[ROI])#-m
        display_buffer = detrend(data_buffer)
        f.set_data(x, display_buffer)
        #plt.ylim(m - (m - min(display_buffer)) * 10, m + (max(display_buffer) - m) * 10)

        psd, freqs = psd_array_multitaper(display_buffer, betaIn.sampling_rate(), fmin=8, fmax=13)        
        F.set_data(freqs, psd)
        plt.pause(1 / sampling_rate)

        time.sleep(0.2)


"""
-------------------------------------------------------------
全チャネル表示
-------------------------------------------------------------

data_buffer = [['' for i in range(500)] for j in range(25)]
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

for i in range(500):
	sample, timestamp = inlet.pull_sample()
	for j in range(25):
		data_buffer[j][i] = (sample[j])


x = np.arange(0, 500, 1)
plt.figure(figsize=(10,6))
for i in range(25):
	plt.plot(x, data_buffer[i])
#plt.ylim(0, 700000)

while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    for i in range(25):
    	data_buffer[i].pop(0)
    	data_buffer[i].append(sample[i])
    	plt.plot(x, data_buffer[i])
    plt.pause(0.001)
"""