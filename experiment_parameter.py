from psychopy import core, visual, event
import pandas as pd
import numpy as np
import itertools
import winsound
from trigger import trigger
import json
import glob

class MIexperiment_components(object):
    def __init__(self, win):
        #channels dict
        self.channels =  {
            'F7':0, 'Fp1':1, 'Fp2':2, 'F8':3, 'F3':4, 'Fz':5, 'F4':6, 'C3':7,
            'Cz':8, 'P8':9, 'P7':10, 'Pz':11, 'P4':12, 'T3':13, 'P3':14, 'O1':15,
            'O2':16, 'C4':17, 'T4':18, 'A2':19, 'ACC20':20, 'ACC21':21, 'ACC22':22,
            'Packet Counter':23, 'TRIGGER':24
            }

        #parameter
        self.N = 512			
        self.blockNum = 1
        self.ready_duration = 1
        self.task_duration = 4
        self.relax_duration = 4
        self.rest_duration = 10
        self.trialNum = 1
        self.baseline_duration = 1
        self.MItask_trial = 1
        self.MRtrial = 1
        self.PTtrial = 1
        self.FB_duration = 1.5
        self.wait_time_list = [.6, .7, .8, .9, 1]

        #DataFrame
        conditions = list(itertools.product(
            range(self.trialNum),
            ('left', 'right'),
        ))
        self.df = pd.DataFrame(
            conditions, columns=('block', 'hand'))
        self.df = self.df.sample(frac=1)
        self.df.sort_values('block', inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        #psychopy初期化
        self.msg = visual.TextStim(win, height=80)

        self.fixation = visual.ShapeStim(
            win, vertices=((-250, 0), (250, 0), (0, 0), (0, -250), (0, 250), (0, 0)),
            fillColor='black', lineColor='black', lineWidth=5)
        
        self.cue = visual.TextStim(win, height=80)

        self.countText = visual.TextStim(
            win, height=100, bold=True, pos=(300,300))

        self.Circle = visual.Circle(
            win, edges=32, fillColor='white', lineColor='white')
        
        self.dummyList = []
        for file in glob.glob('dummy_*.json'):
            with open(file) as f:
                self.dummyList.append(json.loads(f.read()))
        

    def rest(self, win, blocknum):
        trigger.SendTrigger('rest')

        for time in reversed(range(1, self.rest_duration+1)):
            self.msg.setText('Rest\n次は、第' + blocknum + 'ブロックです')
            self.msg.draw()
            self.countText.setText(time)
            self.countText.draw()
            win.flip()

            if time < 4:
                winsound.Beep(1000, 100)

            core.wait(1)


if __name__ == '__main__':
    win = visual.Window(units='pix', fullscr=True, allowGUI=False)

    components = MIexperiment_components(win)
    components.rest(win)