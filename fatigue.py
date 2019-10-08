from psychopy import core, visual, event, sound
import pandas as pd
from trigger import trigger
from experiment_parameter import MIexperiment_components
from instruction import instruction

inst_fatigue = sound.Sound('voicedata/inst_fatigue.wav')
inst_concenterate = sound.Sound('voicedata/inst_concentrate.wav')

def fatigue_VAS(win, components):
    inst_fatigue.play()
    ratingScale = visual.RatingScale(
        win, high=7, size=2.0, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(u'現在の疲労度を\nお答えください。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'疲れを全く\n感じない状態')
        components.msg.setPos((-750, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(u'何もできないほど\n疲れ切っている状態')
        components.msg.setPos((750, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_fatigue.stop()

    fatigue_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)

    inst_concenterate.play()
    ratingScale = visual.RatingScale(
        win, high=7, size=2.0, pos=(0.0, -200), scale=False, labels=False,
        showValue=False, acceptPreText=u'Enter', acceptText='Enter', textSize=0.5, tickMarks=[1, 7],
        markerStart=4, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', noMouse=True)
    while ratingScale.noResponse:
        components.msg.setText(u'現在の集中度を\nお答えください。')
        components.msg.setPos((0, 100))
        components.msg.setHeight(60)
        components.msg.draw()
        components.msg.setText(u'全く集中\nできていない状態')
        components.msg.setPos((-750, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        components.msg.setText(u'非常によく\n集中できている状態')
        components.msg.setPos((750, -200))
        components.msg.setHeight(30)
        components.msg.draw()
        ratingScale.draw()
        win.flip()
    inst_concenterate.stop()

    concentrate_res = ratingScale.getRating()

    components.msg.setPos((0, 0))
    components.msg.setHeight(80)
    
    return fatigue_res, concentrate_res

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)

    print(fatigue_VAS(win, components))
	