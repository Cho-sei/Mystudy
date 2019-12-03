from psychopy import core, visual, event, sound
import pandas as pd
from experiment_parameter import MIexperiment_components
from instruction import instruction

inst_fatigue = sound.Sound('voicedata/inst_fatigue.wav')
inst_concenterate = sound.Sound('voicedata/inst_concentrate.wav')
inst_difficulty = sound.Sound('voicedata/inst_difficulty.wav')
inst_prediction = sound.Sound('voicedata/inst_prediction.wav')

NumkeyList = ['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9']
DeleteList = ['delete', 'num_delete', 'backspace']

def fatigue_VAS(win, components):
    #difficulty
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

    #prediction
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

    #fatigue
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

    #concentrate
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
    
    return fatigue_res, concentrate_res, difficulty_res, prediction_res

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)

    print(fatigue_VAS(win, components))
	