from psychopy import core, visual, event, sound
from experiment_parameter import MIexperiment_components

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)

components.Circle.setRadius(300)
components.Circle.draw()
win.flip()


event.waitKeys(keyList=['space'])