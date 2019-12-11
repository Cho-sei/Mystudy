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

        imgnameList = ['day_flow/スライド' + str(i) for i in range(1, 24)] 
        imgnameList.append('back_right_0')
        self.imgDict = dict([[imgname, visual.ImageStim(self.win, 'InstImage/' + imgname + '.PNG')] for imgname in imgnameList])
        
        self.dummy = [-6.852039504, 3.711962456, -16.51470402, -23.43944568, -23.96121308, -28.59563485, -34.98797214, -31.84493135, 
                      -30.36166352, 2.555086205, 14.56816966, -10.57715854, -10.24612483, 14.17700023, 40.76523032, 42.90205179, 
                      54.87376142, 49.61710255, 53.43006559, 10.53386241, 28.97585958, 43.13693698, 10.50195355, -21.20768374, 
                      -10.5393773, -8.982753082, -0.68323058, 9.240031876, 3.177951254, 9.291938988, -24.33945853, -21.20957587, 
                      -21.28266322, -14.12899582, -3.826137683, -22.378991, -34.31247191, -34.93116256, -37.09434031, -9.442296083, -11.458945]

    def introduction(self, day):
        if day == 'Day1':
            self.PresentText(text=u'実験開始', sound='ex_start')
            self.PresentImg(img='day_flow/スライド1', sound='ex_flow_into_day1')
        elif day == 'Day2':
            self.PresentImg(img='day_flow/スライド2', sound='ex_flow_into_day2')
        else:
            self.PresentImg(img='day_flow/スライド3', sound='ex_flow_into_day3')
    
    def inst_questionnaire(self, timing=None):
        if timing != None:
            ratingScale = visual.RatingScale(
                self.win, low=-1, high=1, labels=[u'左', u'どちらも', u'右'], pos=(0.0, -200),
                scale=False, showValue=False, acceptPreText='Enter', acceptText='Enter',
                markerStart=0, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return',
                marker=visual.TextStim(self.win, text=u'「1」 ⇦ ▼ ⇨ 「3」\n\n', units='norm'), noMouse=True)
            ratingScale.draw()
            self.PresentText(text=u'アンケート', sound='inst_questionnaire')
        else:
            self.PresentText(text=u'アンケート', sound='into_questionnaire')
        self.PresentText(text='Ready', sound='start')

    def inst_flandars(self):
        ratingScale = visual.RatingScale(
            self.win, low=-1, high=1, labels=[u'左', u'どちらも', u'右'], pos=(0.0, -200),
            scale=False, showValue=False, acceptPreText='Enter', acceptText='Enter',
            markerStart=0, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return',
            marker=visual.TextStim(self.win, text=u'「1」 ⇦ ▼ ⇨ 「3」\n\n', units='norm'), noMouse=True)
        ratingScale.draw()
        self.PresentText(text=u'利き手判別テスト', sound='into_flandars')
        self.PresentText(text='Ready', sound='start')
    
    def inst_KVIQ(self, timing=None):
        if timing == 'pre':
            KVIQ_inst.instruction(self.win)
        self.PresentText(text=u'運動イメージ能力検査', sound='into_KVIQ')
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
        self.PresentText(text=u'メンタルローテーション', sound='into_MR')
        self.PresentText(text='Ready', sound='start')
    
    def inst_PT(self, timing=None):
        if timing == 'pre':
            self.PresentText(text=u'運動パフォーマンス\nテスト', sound='into_inst_PT')
            event.waitKeys(keyList=['return'])
            self.PlaySound('inst_PT')
            self.PresentImg(img='day_flow/スライド5', sound='inst_PT_borad')
            self.PresentText(text='Relax', sound='viz_relax')
            self.PresentText(text=' Left \n   or   \n Right', sound='inst_PT_cue')
            self.PresentImg(img='day_flow/スライド6', sound='inst_PT_right')
            self.PresentImg(img='day_flow/スライド7', sound='inst_PT_first')
            self.PresentImg(img='day_flow/スライド8', sound='inst_PT_second')
            self.PresentImg(img='day_flow/スライド9', sound='inst_PT_rightside')
            self.PresentImg(img='day_flow/スライド10', sound='inst_PT_rotate')
            self.PresentImg(img='day_flow/スライド11', sound='inst_PT_rotate_all')
            self.PresentImg(img='day_flow/スライド18', sound='inst_PT_last')
            self.PresentImg(img='day_flow/スライド12', sound='inst_PT_last_all')
            self.PresentImg(img='day_flow/スライド13', sound='inst_PT_enter')
            self.PresentText(text='Left', sound='inst_PT_left')
            self.PresentImg(img='day_flow/スライド14', sound='inst_PT_left_first')
            self.PresentImg(img='day_flow/スライド15', sound='inst_PT_left_rotate')
            self.PresentImg(img='day_flow/スライド16', sound='inst_PT_left_enter')
            self.PresentImg(img='day_flow/スライド7', sound='prac_PT_right_first', wait_time=2)
            self.PresentImg(img='day_flow/スライド8', sound='prac_PT_right_second', wait_time=2)
            self.PresentImg(img='day_flow/スライド9', sound='prac_PT_right_third', wait_time=4)
            self.PresentImg(img='day_flow/スライド10', sound='prac_PT_right_rotate', wait_time=2)
            self.PresentImg(img='day_flow/スライド11', sound='prac_PT_right_rotateall', wait_time=4)
            self.PresentImg(img='day_flow/スライド17', sound='prac_PT_right_last')
            event.waitKeys(keyList=['return'])
            self.PresentImg(img='day_flow/スライド19', sound='move_tenkey')
            event.waitKeys(keyList=['return'])
            self.PresentImg(img='day_flow/スライド14', sound='prac_PT_left_first', wait_time=3)
            self.PresentImg(img='day_flow/スライド15', sound='prac_PT_left_rotate', wait_time=4)
            self.PresentImg(img='day_flow/スライド16', sound='prac_PT_left_last')
            event.waitKeys(keyList=['return'])
            self.win.flip()
            self.PresentText(text=u'できる限り早く\n課題を行ってください', sound='confirmation_PT')
            event.waitKeys(keyList=['return'])
        self.PresentText(text=u'運動パフォーマンス\nテスト', sound='into_PT')
        self.PresentText(text='Ready', sound='start')
    
    def inst_train_proc(self):
        self.PresentImg(img='day_flow/スライド4', sound='inst_training_proc')
    
    def inst_MItest(self, lateral=None, timing=None):
        if (timing == 'pre') & (lateral != None):
            if lateral == 'right':
                self.PresentText(text=u'運動イメージ課題', sound='into_inst_MItest_right')            
            else:
                self.PresentText(text=u'運動イメージ課題', sound='into_inst_MItest_left')            
            self.PresentText(text='Relax', sound='viz_relax')
            self.components.fixation.draw()
            self.win.flip()
            self.PlaySound('viz_fixation')
            self.PresentText(text='Relax', sound='repeat')
            self.PresentText(text=u'練習', sound='into_prac')
            self.PresentText(text='Relax', sound='prac_relax', wait_time=2)
            self.PlaySound('prac_MI', wait_time=2)
            self.components.fixation.draw()
            self.win.flip()
            event.waitKeys(keyList=['return'])
            self.PresentText(text='', sound='otsukaresama')
        else:
            self.PresentText(text=u'運動イメージ課題', sound='into_MItest')
            self.PresentText(text='Ready', sound='start')
    
    def inst_resting(self):
        self.PresentText(text=u'安静時脳波の測定', sound='inst_resting')
        self.PresentText(text='Ready', sound='start')
    
    def inst_training(self, lateral=None):
        if lateral != None:
            self.PresentText(text=u'運動イメージ\nトレーニング', sound='into_inst_training')
            if lateral == 'right':
                self.PresentImg(img='day_flow/スライド23', sound='inst_training_right')
            else:
                self.PresentImg(img='day_flow/スライド23', sound='inst_training_left')
            self.soundDict['FB_NFB'].play()
            self.viz_circle(self.soundDict['FB_NFB'].getDuration() + 1)
            self.PresentText(text='', sound='confirmation')
        else:
            self.PresentText(text=u'運動イメージ\nトレーニング', sound='into_training')
            self.PresentText(text='Ready', sound='start')
    
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
    
    def PresentText(self, text, sound, wait_time=1):
        self.components.msg.setPos((0, 0))
        self.components.msg.setText(text)
        self.components.msg.draw()
        self.win.flip()
        self.PlaySound(sound, wait_time)
    
    def PresentImg(self, img, sound, wait_time=1):
        self.imgDict[img].draw()
        self.win.flip()
        self.PlaySound(sound, wait_time)

    def PlaySound(self, soundname, wait_time=1):
        self.soundDict[soundname].play()
        core.wait(self.soundDict[soundname].getDuration() + wait_time)

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)
    #instruction.inst_training('continuous')
    instruction.PlaySound('otsukaresama')