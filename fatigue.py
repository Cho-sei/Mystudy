from psychopy import core, visual, event, sound
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction

inst_fatigue = sound.Sound('voicedata/inst_fatigue.wav')
inst_concenterate = sound.Sound('voicedata/inst_concentrate.wav')
inst_difficulty = sound.Sound('voicedata/inst_difficulty.wav')
inst_prediction = sound.Sound('voicedata/inst_prediction.wav')
inst_expectation = sound.Sound('voicedata/inst_expectation.wav')
inst_serve_lateral = sound.Sound('voicedata/inst_serve_lateral.wav')

NumkeyList = ['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9']
DeleteList = ['delete', 'num_delete', 'backspace']

def expectation(win, components):
    inst_expectation.play()
    ratingScale = visual.RatingScale(
        win, high=7, size=1.5, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(u'このトレーニングの効果を\nどれほど期待していますか。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'全く\n期待していない')
        components.msg.setPos((-500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(u'非常に\n期待している')
        components.msg.setPos((500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_expectation.stop()

    expectation_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return expectation_res

def lateral(win, components):
    img = visual.ImageStim(win, 'InstImage/tennis_court.png', size=500)
    inst_serve_lateral.play()
    ratingScale = visual.RatingScale(
        win, low=0, high=1, size=0.8, pos=(0.0, -280), scale=False, labels=['左', '右'], 
        markerStart=0.5, showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=1.5,
        leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        img.draw()
        components.msg.setText(u'右からのサーブと左からのサーブでは\nどちらがより得意ですか。')
        components.msg.setPos((0, 300))
        components.msg.setHeight(40)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_serve_lateral.stop()

    lateral_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return lateral_res

def difficulty(win, components):
    inst_difficulty.play()
    ratingScale = visual.RatingScale(
        win, high=7, size=1.5, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(u'運動のイメージは\n難しかったですか。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'非常に簡単')
        components.msg.setPos((-500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(u'非常に難しい')
        components.msg.setPos((500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_difficulty.stop()

    difficulty_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return difficulty_res

def prediction(win, components):
    inst_prediction.play()
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
    inst_prediction.stop()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return prediction_res

def fatigue_func(win, components):
    inst_fatigue.play()
    ratingScale = visual.RatingScale(
        win, high=7, size=1.5, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(u'現在の疲労度を\nお答えください。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'疲れを全く\n感じない状態')
        components.msg.setPos((-500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(u'何もできないほど\n疲れ切っている状態')
        components.msg.setPos((500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_fatigue.stop()

    fatigue_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return fatigue_res

def concentrate(win, components):
    inst_concenterate.play()
    ratingScale = visual.RatingScale(
        win, high=7, size=1.5, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(u'現在の集中度を\nお答えください。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'全く集中\nできていない状態')
        components.msg.setPos((-500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(u'非常によく\n集中できている状態')
        components.msg.setPos((500, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_concenterate.stop()

    concentrate_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    return concentrate_res

def pre_ques(win, components):
    expectation_res = expectation(win, components)
    fatigue_res = fatigue_func(win, components)

    return expectation_res, fatigue_res

def fatigue_VAS(win, components):
    difficulty_res = difficulty(win, components)
    prediction_res = prediction(win, components)
    fatigue_res = fatigue_func(win, components)
    concentrate_res = concentrate(win, components)

    return fatigue_res, concentrate_res, difficulty_res, prediction_res

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)

    print(pre_ques(win, components))
	