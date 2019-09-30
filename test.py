from psychopy import core, visual, event
from experiment_parameter import MIexperiment_components

win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)

waitinig_key = True
while waitinig_key:
	keys = event.getKeys(keyList=['return'])
	if 'return' in keys:
		components.msg.setText('press')
		components.msg.draw()
		win.flip()
		waitinig_key = False

core.wait(1)