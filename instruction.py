from psychopy import core, visual, event, sound
from experiment_parameter import MIexperiment_components
import KVIQ_inst
import flandars
import os
import pathlib

class instruction():
    def __init__(self, win, components):
        self.win = win
        self.components = components

        soundnameList = [f.stem for f in pathlib.Path('voicedata').glob('*.wav')]
        self.soundDict = dict([[soundname, sound.Sound('voicedata/' + soundname + '.wav')] for soundname in soundnameList])

        imgnameList = ['proc_day1', 'proc_day2', 'proc_day3', 'back_right_0']
        self.imgDict = dict([[imgname, visual.ImageStim(self.win, 'InstImage/' + imgname + '.png')] for imgname in imgnameList])
        
        self.dummy = [-6.852039504, 3.711962456, -16.51470402, -23.43944568, -23.96121308, -28.59563485, -34.98797214, -31.84493135, 
                      -30.36166352, 2.555086205, 14.56816966, -10.57715854, -10.24612483, 14.17700023, 40.76523032, 42.90205179, 
                      54.87376142, 49.61710255, 53.43006559, 10.53386241, 28.97585958, 43.13693698, 10.50195355, -21.20768374, 
                      -10.5393773, -8.982753082, -0.68323058, 9.240031876, 3.177951254, 9.291938988, -24.33945853, -21.20957587, 
                      -21.28266322, -14.12899582, -3.826137683, -22.378991, -34.31247191, -34.93116256, -37.09434031, -9.442296083, -11.458945]

    def introduction(self, day):
        if day == 'Day1':
            self.PresentText(text=u'実験開始', sound='ex_start')
            self.PresentImg(img='proc_day1', sound='ex_flow_into_day1')
        elif day == 'Day2':
            self.PresentImg(img='proc_day2', sound='ex_flow_into_day2')
        else:
            self.PresentImg(img='proc_day3', sound='ex_flow_into_day3')
        
    def inst_flandars(self):
        ratingScale = visual.RatingScale(
            self.win, low=-1, high=1, labels=[u'左', u'どちらも', u'右'], scale=False, pos=(0.0, -200),
            showValue=False, acceptPreText=u'バーをクリック', acceptText='OK', noMouse=True)
        ratingScale.draw()
        self.PresentText(text=u'利き手判別テスト', sound='into_flandars')
        self.PresentText(text='Ready', sound='start')
    
    def inst_KVIQ(self):
        KVIQ_inst.instruction(self.win)
        self.PresentText(text='Ready', sound='start')
    
    def inst_MR(self, timing=None):
        if timing == 'pre':
            self.PresentText(text=u'メンタルローテーション', sound='into_inst_MR')
            self.components.fixation.draw()
            self.win.flip()
            self.PlaySound('MR_fixation')
            self.PresentImg(img='back_right_0', sound='MR_figure')
            self.imgDict['back_right_0'].draw()
            self.components.msg.setText(u'左手→１')
            self.components.msg.setPos((-250, -300))
            self.components.msg.draw()
            self.components.msg.setText(u'３←右手')
            self.components.msg.setPos((250, -300))
            self.components.msg.draw()
            self.win.flip()
            self.PlaySound('MR_tenkey')
            self.components.fixation.draw()
            self.win.flip()
            self.PlaySound('MR_repeat')
        self.PresentText(text='Ready', sound='into_MR')
        self.PlaySound('start')
    
    def inst_PT(self, timing=None):
        self.PresentText(text=u'運動パフォーマンス\nテスト', sound='into_inst_PT')
        event.waitKeys(keyList=['return'])
        if timing == 'pre':
            self.PlaySound('inst_PT')
        self.PresentText(text='Ready', sound='into_PT')
        self.PlaySound('start')
    
    def inst_MItest(self, timing=None):
        if timing == 'pre':
            self.PresentText(text=u'運動想起テスト', sound='into_inst_MItest')            
            self.PresentText(text='Relax', sound='viz_relax')
            self.PresentText(text=' Left\n  or\nRight', sound='inst_cue')
            self.components.fixation.draw()
            self.win.flip()
            self.PlaySound('viz_fixation')
            self.PresentText(text='Relax', sound='repeat')
        else:
            self.PresentText(text='Ready', sound='into_MItest')
            self.PlaySound('start')
    
    def inst_resting(self):
        self.PresentText(text=u'安静時脳波の測定', sound='inst_resting')
        self.PresentText(text='Ready', sound='start')
    
    def inst_training(self, condition=None):
        if condition != None:
            self.PresentText(text=u'運動想起トレーニング', sound='into_inst_training')
            if condition == 'control':
                self.soundDict['FB_control'].play()
                self.viz_circle(self.soundDict['FB_control'].getDuration() + 1)
            elif condition == 'discrete':
                self.soundDict['FB_discrete'].play()
                self.viz_circle(self.soundDict['FB_discrete'].getDuration() + 1)
                self.PresentText(text=' GOOD!\n  or\nBAD...', sound='FB_discrete_FB')
            else:
                self.soundDict['FB_NFB'].play()
                self.viz_circle(self.soundDict['FB_NFB'].getDuration() + 1)
            self.PresentText(text='', sound='confirmation')
        else:
            self.PresentText(text='Ready', sound='into_training')
            self.PlaySound('start')
    
    def inst_finish(self, day):
        if day == 'Day3':
            self.PresentText(text='Finish', sound='ex_finish_all')
        else:
            self.PresentText(text='Finish', sound='ex_finish')
    
    
    
    def viz_circle(self, soundDuration):
        clock = core.Clock()
        t_start = clock.getTime()
        t_duration = clock.getTime() - t_start

        j = 0
        while t_duration < soundDuration:	
                self.components.Circle.setRadius(5*self.dummy[j] + 300)
                self.components.Circle.draw()
                self.components.fixation.draw()
                core.wait(.1)
                self.win.flip()
                j += 1
                if j == len(self.dummy):
                    j = 0
                t_duration = clock.getTime() - t_start
    
    def PresentText(self, text, sound):
        self.components.msg.setPos((0, 0))
        self.components.msg.setText(text)
        self.components.msg.draw()
        self.win.flip()
        self.PlaySound(sound)
    
    def PresentImg(self, img, sound):
        self.imgDict[img].draw()
        self.win.flip()
        self.PlaySound(sound)

    def PlaySound(self, soundname, wait_time=1):
        self.soundDict[soundname].play()
        core.wait(self.soundDict[soundname].getDuration() + wait_time)

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)
    instruction.inst_MR()