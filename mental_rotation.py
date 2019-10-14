from psychopy import core, visual, event
import pandas as pd
import itertools
import sys
from experiment_parameter import MIexperiment_components

def hand_lateralization_task(win, components, timing):
    #DataFrame
    conditions = list(itertools.product(
        range(components.MRtrial),
        ('left', 'right'),
        ('palm', 'back'),
        (0, 60, 120, 180, 240, 300),
    ))
    df = pd.DataFrame(
        conditions, columns=('view', 'hand', 'face', 'angle'))
    df = df.sample(frac=1)
    df = df.sort_values('view')
    df.reset_index(drop=True, inplace=True)

    Image = visual.ImageStim(win)

    components.msg.setText('Start')
    components.msg.draw()
    win.flip()

    core.wait(components.ready_duration)

    clock = core.Clock()

    response = []
    RT = []
    for i, row in df.iterrows():
        components.fixation.draw()
        win.flip()

        core.wait(1)

        Image.setImage('HandImg/' + row['face'] + '_' + row['hand'] + '_' + str(row['angle']) + '.png')
        Image.draw()
        win.flip()

        t_start = clock.getTime()
        key = event.waitKeys(keyList=['1', 'num_1', '3', 'num_3'])
        RT.append(clock.getTime() - t_start)
        if row['hand'] == 'left':
            if ('1' in key ) or ('num_1' in key):
                response.append(True)
            else:
                response.append(False)
        else:
            if ('3' in key ) or ('num_3' in key):
                response.append(True)
            else:
                response.append(False)
    df['response'] = response
    df['RT'] = RT
    df['timing'] = timing
    
    return df[['timing', 'view', 'hand', 'face', 'angle', 'response', 'RT']]

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)

    testdf = hand_lateralization_task(win, components, 'pre')
    testdf.to_csv('test.csv')
    testdf = hand_lateralization_task(win, components, 'post')
    MR_df = pd.read_csv('test.csv', index_col=0)
    MR_result = pd.concat([MR_df, testdf])
    MR_result.to_csv('test.csv')
