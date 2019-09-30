from psychopy import core, visual, event
from experiment_parameter import MIexperiment_components

event.globalKeys.add(key='escape', func=core.quit)

win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
components = MIexperiment_components(win)

waitinig_key = True
clock = core.Clock()
t_start = clock.getTime()
while waitinig_key:
	t = clock.getTime() - t_start
	keys = event.waitKeys(keyList=['return'])
	if 'return' in keys:
		components.msg.setText(t)
		components.msg.draw()
		win.flip()
		waitinig_key = False

core.wait(1)