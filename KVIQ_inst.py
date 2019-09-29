from psychopy import core, visual, event, sound

soundnameList = ['KVIQ_inst_start', 'KVIQ_inst_finish', 'KVIQ_inst_eval', 'KVIQ_inst_imagery',
                'KVIQ_inst_move', 'KVIQ_inst_pre', 'KVIQ_inst_scale', 'KVIQ_inst_flow']
soundDict = dict([[soundname, sound.Sound('voicedata/' + soundname + '.wav')] for soundname in soundnameList])

def instruction(win):
    inst_text = visual.TextStim(win, u'運動イメージ検査', height=80)
    proc_img = []
    proc_sizeList = [[1600, 236.4], [411, 666], [309, 666], [513.6, 667.8], [405, 670.2]]
    proc_posList = [[0, 300], [-580, -150], [-220, -150], [200, -150], [580, -150]]
    for i, (size, pos) in enumerate(zip(proc_sizeList, proc_posList)):
        proc_img.append(visual.ImageStim(win, image='InstImage/KVIQ_inst_proc_'+str(i)+'.png',
        size=(size[0], size[1]), pos=(pos[0], pos[1])))
    eval_img = visual.ImageStim(win, image='InstImage/KVIQ_inst_eval.png', size=(16*100,9*100))

    proc_soundList = ['KVIQ_inst_flow', 'KVIQ_inst_pre', 'KVIQ_inst_move', 
                        'KVIQ_inst_imagery', 'KVIQ_inst_eval', ]
    proc_opaList = [[1]*5,
                    [1.0, 1.0, 0.5, 0.5, 0.5],
                    [1.0, 0.5, 1.0, 0.5, 0.5],
                    [1.0, 0.5, 0.5, 1.0, 0.5],
                    [1.0, 0.5, 0.5, 0.5, 1.0]]

    display_and_sound(win, inst_text, soundDict['KVIQ_inst_start'])
    for sound, opa in zip(proc_soundList, proc_opaList):
        display_and_sound(win, proc_img, soundDict[sound], opa)
    display_and_sound(win, eval_img, soundDict['KVIQ_inst_scale'])
    soundDict['KVIQ_inst_finish'].play()
    core.wait(soundDict['KVIQ_inst_finish'].getDuration() + 1)


def display_and_sound(win, img, sound, opacity=None):
    if type(img) == list:
        for image, opa in zip(img, opacity):
            image.setOpacity(opa)
            image.draw()
    else:
        img.draw()
    win.flip()

    sound.play()
    core.wait(sound.getDuration() + 1)


if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)

    instruction(win)