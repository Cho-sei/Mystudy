from psychopy import core, visual, event, sound
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction
import os
import pathlib

soundnameList = [f.stem for f in pathlib.Path('voicedata').glob('*.wav')]
soundDict = dict([[soundname, sound.Sound('voicedata/' + soundname + '.wav')] for soundname in soundnameList])

question_list = {'fatigue':[u'現在の疲労度を\nお答えください。', u'全く疲れを\n感じない状態', u'何もできないほど\n疲れ切っている状態', 'inst_fatigue'],
                 'concentrate':[u'現在の集中度を\nお答えください。', u'全く集中\nできていない状態', u'非常によく\n集中できている状態', 'inst_concentrate'], 
                 'difficulty':[u'運動のイメージは\n難しかったですか。', u'非常に簡単', u'非常に難しい', 'inst_difficulty'], 
                 'interest':[u'このトレーニングに対して\nどれほど興味をお持ちですか。', u'全く\n興味がない', u'非常に\n興味がある', 'inst_interest'],
                 'expectation':[u'このトレーニングに\nどれほど期待していますか。', u'全く\n期待していない', u'非常に\n期待している', 'inst_expectation'],
                 'motivation':[u'このトレーニングに対して\nどれほど意欲がありますか。', u'全くない', u'非常にある', 'inst_motivation'],
                 'anxiety':[u'このトレーニングに対して\n不安を感じていますか。', u'全く感じていない', u'非常に感じている', 'inst_anxiety'],
                 'sleepiness':[u'現在の眠気を\nお答えください。', u'非常に目が\n覚めている', u'非常に眠い', 'inst_sleepiness']
                 }

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

NumkeyList = ['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9']
DeleteList = ['delete', 'num_delete', 'backspace']

def rating_questionnaire(win, components, question, low_text, high_text, sound, max_value=7):
    soundDict[sound].play()
    ratingScale = visual.RatingScale(
        win, high=max_value, size=1.5, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(question)
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(low_text)
        components.msg.setPos((-500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(high_text)
        components.msg.setPos((500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    soundDict[sound].stop()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return ratingScale.getRating()

def KVIQ_ratingscale(win):
    response = []
    for content, instruction, soundname in zip(choices, inst, ['question_visual', 'question_kinesthetic']):
        soundDict[soundname].play()
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
        soundDict[soundname].stop()
        response.append(ratingScale.getRating())
    return response

def prediction(win, components):
    soundDict['inst_prediction'].play()
    Enter_num = visual.TextStim(win, height=100, bold=True, pos=(0, -200), color='blue')
    Enter_num.setText('')
    wait_return = True
    while wait_return:
        components.msg.setText(u'運動イメージの確信度をお答えください。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'0 ～ 100の範囲で、\n数字を入力してEnterを押してください。')
        components.msg.setPos((0, 0))
        components.msg.setHeight(50)
        components.msg.draw()
        components.msg.setText(u'%')
        components.msg.setPos((100, -200))
        components.msg.setHeight(50)
        components.msg.draw()
        keys = event.getKeys(keyList=['return']+NumkeyList+DeleteList)
        for key in keys:
            if (key in NumkeyList) & (len(Enter_num.text) < 2):
                Enter_num.text += str(NumkeyList.index(key))
            elif key in DeleteList:
                Enter_num.text = Enter_num.text[:-1]
        if (len(Enter_num.text) != 0) & ('return' in keys):
            prediction_res = Enter_num.text
            wait_return = False
        Enter_num.draw()
        win.flip()
    soundDict['inst_prediction'].stop()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return prediction_res

def attribute_question(win, components):
    expectation_res = rating_questionnaire(win, components, *question_list['expectation'])
    interest_res = rating_questionnaire(win, components, *question_list['interest'])
    motivation_res = rating_questionnaire(win, components, *question_list['motivation'])
    anxiety_res = rating_questionnaire(win, components, *question_list['anxiety'])

    return pd.Series({'expectation':expectation_res,
                         'interest':interest_res,
                         'motivation':motivation_res,
                         'anxiety':anxiety_res})

def fatigue_VAS(win, components):
    visual_res, kinethestic_res = KVIQ_ratingscale(win)
    difficulty_res = rating_questionnaire(win, components, *question_list['difficulty'])
    prediction_res = prediction(win, components)
    fatigue_res = rating_questionnaire(win, components, *question_list['fatigue'])
    concentrate_res = rating_questionnaire(win, components, *question_list['concentrate'])
    sleepiness_res = rating_questionnaire(win, components, *question_list['sleepiness'])

    return pd.Series({'fatigue':fatigue_res,
                      'concentrate':concentrate_res,
                      'difficulty':difficulty_res,
                      'prediction':prediction_res,
                      'sleepiness':sleepiness_res,
                      'VisualScale':visual_res,
                      'KinethesticScale':kinethestic_res})

def pre_train_question(win, components):
    fatigue_res = rating_questionnaire(win, components, *question_list['fatigue'])
    concentrate_res = rating_questionnaire(win, components, *question_list['concentrate'])
    sleepiness_res = rating_questionnaire(win, components, *question_list['sleepiness'])

    return pd.Series({'fatigue':fatigue_res,
                      'concentrate':concentrate_res,
                      'sleepiness':sleepiness_res})

def post_question(win, components):
    expectation_res = rating_questionnaire(win, components, *question_list['expectation'])

    return pd.Series({'expectation': expectation_res})

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    
    print(attribute_question(win, components))
	