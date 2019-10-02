from psychopy import core, visual, event, sound
import pandas as pd

soundnameList = ['MItest_pre','MItest_1','MItest_2','MItest_3_right','MItest_3_left',
            'MItest_4_right','MItest_4_left','MItest_5_right','MItest_5_left',
            'MItest_imagery', 'MItest_release', 'question_visual', 'question_kinesthetic', 'PT_start']
soundDict = dict([[soundname, sound.Sound('voicedata/' + soundname + '.wav')] for soundname in soundnameList])

def display_ratingscale(win, choices, inst):
    response = []
    for content, instruction, soundname in zip(choices, inst, ['question_visual', 'question_kinesthetic']):
        soundFlag = True
        inst_text = visual.TextStim(win, instruction, pos=(0.0, 250), height=60)
        ratingScale = visual.RatingScale(
            win, high=5, size=2.0, labels=False, pos=(0.0, -100), scale=False,
            showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5,
            markerStart=3, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
        while ratingScale.noResponse:
            inst_text.draw()
            for j, text in enumerate(content):
                contents = visual.TextStim(win, text, pos=(j*280-560, 100), height=30)
                contents.draw()
            ratingScale.draw()
            win.flip()
            if soundFlag:
                soundDict[soundname].play()
                soundFlag = False
        soundDict[soundname].stop()
        response.append(ratingScale.getRating())
    return response

def play_sound(win, sound_list, wait_time, images=[]):
    arrow = visual.ShapeStim(
        win, vertices=((-30, 10), (0, 10), (0, 25), (30, 0), (0, -25), (0, -10), (-30, -10)),
        fillColor='white', lineColor='white')
    text = visual.TextStim(win, height=80)
    for i, (soundname, time) in enumerate(zip(sound_list, wait_time)):
        if i == 0:
            if len(images) == 2:
                images[0].setPos((-400, -100))
                images[0].draw()
                win.flip()
        elif i == 1:
            if len(images) == 2:
                for i, x_pos in enumerate([-400, 400]):
                    images[i].setPos((x_pos, -100))
                    images[i].draw()
                    arrow.setPos((0, -100))
                    arrow.draw()
            elif len(images) == 4:
                for i, (x_pos, arrow_pos) in enumerate(zip([-600, -200, 200, 600], [-400, 0, 400, 0])):
                    images[i].setPos((x_pos, -100))
                    images[i].draw()
                    arrow.setPos((arrow_pos, -100))
                    arrow.draw()
            win.flip()
        elif (i == 2) | (i == 3):
            text.setText(u'実際に運動')
            text.draw()
            win.flip()
        else:
            text.setText(u'イメージ')
            text.draw()
            win.flip()

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
    imagenameList = ['base-left', 'base-right', '1-left', '1-right', '2-left', '2-right', '3-left', '3-right', '4-left', '4-right',
                     'index-finger-left', 'index-finger-right', 'middle-finger-left', 'middle-finger-right', 'ring-finger-left',
                     'ring-finger-right', 'little-finger-left', 'little-finger-right']
    imageDict = dict([[imagename, visual.ImageStim(win, 'InstImage/' + imagename + '.jpg', size=(300, 617.1))] for imagename in imagenameList])

    summary = pd.DataFrame(columns=['hand', 'part', 'VR', 'KR'])

    handers = ['left', 'right'] if handed == 'left' else ['right', 'left']
    
    for i, hand in enumerate(handers):
        
        img_list = [['base-', '1-'],
                    ['base-', '2-'],
                    ['base-', '3-'],
                    ['base-', '4-'],
                    ['index-finger-', 'middle-finger-', 'ring-finger-', 'little-finger-']]
        
        for k in range(len(img_list)):
            for l in range(len(img_list[k])):
                img_list[k][l] = img_list[k][l] + hand

        for j, (text, image) in enumerate(zip([u'頸部の屈曲・伸展', u'肩甲骨の拳上', u'肩関節の屈曲', u'肘関節の屈曲', u'母指と他指の対立'], img_list)):
            if ( i == 1 ) & (j < 2):
                continue
            MItext = visual.TextStim(win, text, height=80, bold=True, pos=(0, 300))
            MItext.setAutoDraw(True)
            win.flip()

            sound_list = ['MItest_pre']
            sound_list.append('MItest_'+str(j+1)) if j < 2 else sound_list.append('MItest_'+str(j+1)+'_'+hand)
            sound_list.append('PT_start')
            sound_list.append('MItest_release')
            sound_list.append('MItest_imagery')
            sound_list.append('PT_start')

            play_sound(win, sound_list, [2, 2, 5, 1, 1, 5], [imageDict[img] for img in image])
            MItext.setAutoDraw(False)

            response = display_ratingscale(win, choices, inst)
            series = pd.Series([hand, j+1, response[0], response[1]], index=summary.columns)

            summary = summary.append(series, ignore_index=True)

    summary['timing'] = timing
    return summary[['timing', 'hand', 'part', 'VR', 'KR']]
    

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    
    KVIQ_proc(win, 'right', 'pre')
