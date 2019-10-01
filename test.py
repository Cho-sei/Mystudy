from psychopy import core, visual, event, sound
#from experiment_parameter import MIexperiment_components

win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
event.waitKeys(keyList=['space'])