from psychopy import core, visual, event, sound
import pandas as pd

soundnameList = ['MItest_pre','MItest_1','MItest_2','MItest_3_right','MItest_3_left',
            'MItest_4_right','MItest_4_left','MItest_5_right','MItest_5_left',
            'MItest_imagery', 'question_visual', 'question_kinesthetic']
soundDict = dict([[soundname, sound.Sound('voicedata/' + soundname + '.wav')] for soundname in soundnameList])

def display_ratingscale(win, choices, inst):
    response = []
    for content, instruction, soundname in zip(choices, inst, ['question_visual', 'question_kinesthetic']):
        soundFlag = True
        inst_text = visual.TextStim(win, instruction, pos=(0.0, 250), height=60)
        ratingScale = visual.RatingScale(
            win, high=5, size=2.0, labels=False, scale=False, pos=(0.0, -100),
            showValue=False, acceptPreText=u'バーをクリック', acceptText='OK')
        while ratingScale.noResponse:
            inst_text.draw()
            for j, text in enumerate(content):
                contents = visual.TextStim(win, text, pos=(j*280-560, 100), height=30)
                contents.draw()
            ratingScale.draw()
            win.flip()
            if soundFlag:
                play_sound([soundname], [0])
                soundFlag = False
        response.append(ratingScale.getRating())
    return response

def play_sound(sound_list, wait_time):
    for soundname, time in zip(sound_list, wait_time):
        soundDict[soundname].play()
        core.wait(soundDict[soundname].getDuration() + time)

def KVIQ_proc(win, handed, timing):
    inst = [u'視覚イメージはどれくらいはっきりとイメージできましたか。',
            u'運動した感覚はどれくらいしっかりと感じましたか。']
    choices = [[u'イメージ\nできない',
                u'ぼんやりと\nイメージできる',
                u'ある程度\nはっきりと\nイメージできる',
                u'はっきりと\nイメージできる',
                u'見ているのと\n同じくらい、\nはっきりと\nイメージできる'],
               [u'感じない',
                u'少し感じる',
                u'ある程度\n感じる',
                u'しっかりと\n感じる',
                u'運動を行っているのと\n同じくらい、\nしっかりと\n感じる']]

    summary = pd.DataFrame(columns=['hand', 'part', 'VR', 'KR'])

    handers = ['left', 'right'] if handed == 'left' else ['right', 'left']
    for i, hand in enumerate(handers):
        for j, text in enumerate([u'頸部の屈曲・伸展', u'肩甲骨の拳上', u'肩関節の屈曲', u'肘関節の屈曲', u'母指と他指の対立']):
            if ( i == 1 ) & (j < 2):
                continue
            MItext = visual.TextStim(win, text, height=80, bold=True)
            MItext.draw()
            win.flip()

            sound_list = ['MItest_pre']
            sound_list.append('MItest_'+str(j+1)) if j < 2 else sound_list.append('MItest_'+str(j+1)+'_'+hand)
            sound_list.append('PT_start', 'MItest_imagery', 'PT_start')
            play_sound(sound_list, [1, 1, 5, 1, 5])

            response = display_ratingscale(win, choices, inst)
            series = pd.Series([hand, j+1, response[0], response[1]], index=summary.columns)

            summary = summary.append(series, ignore_index=True)

    summary['timing'] = timing
    return summary[['timing', 'hand', 'part', 'VR', 'KR']]
    

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    
    KVIQ_proc(win, 'right').to_csv('sha3_KVIQ_post.csv')
