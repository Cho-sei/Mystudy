from psychopy import core, visual, event, sound
from experiment_parameter import MIexperiment_components

win = visual.Window(units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)

keys = event.waitKeys()
components.msg.setText(keys)
components.msg.draw()
win.flip()

core.wait(1)


