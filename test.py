from psychopy import core, visual, event, sound
#from experiment_parameter import MIexperiment_components


win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)

ratingScale = visual.RatingScale(
    win, high=5, size=2.0, labels=False, scale=False, pos=(0.0, -100),
    showValue=False, acceptPreText=u'バーをクリック', acceptText='OK',
    markerStart=3, leftKeys='num_1', rightKeys = 'num_3', acceptKeys='return', 
    marker=visual.TextStim(win, text=u'1 ←▼→ 3\n\n', units='norm'), markerColor='black')
while ratingScale.noResponse:
    ratingScale.draw()
    win.flip()
