from psychopy import core, visual, event, sound
import itertools
import pandas as pd
from experiment_parameter import MIexperiment_components

def performance_test(win, components, timing, handed):
    #DataFrame
    trial_proc = ('left', 'right') if handed == 'left' else ('right', 'left')
    conditions = list(itertools.product(
        range(components.PTtrial),
        trial_proc,
    ))
    df = pd.DataFrame(
        conditions, columns=('trial', 'hand'))
    
    clock = core.Clock()

    components.msg.setText('Start')
    components.msg.draw()
    win.flip()

    core.wait(1)

    PTime = []
    for i, row in df.iterrows():

        components.fixation.draw()
        win.flip()

        core.wait(1)

        components.msg.setText(row['hand'])
        components.msg.draw()
        win.flip()

        t_start = clock.getTime()
        key = event.waitKeys(keyList=['return'])
        PTime.append(clock.getTime() - t_start)

    df['PTime'] = PTime
    df['timing'] = timing

    return df[['timing', 'trial', 'hand', 'PTime']]


if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)

    Ptest_df = performance_test(win, components, 'pre', 'right')
    Ptest_df.to_csv('result/test_Ptest.csv')

    Ptest_df_post = performance_test(win, components, 'post', 'right')
    PT_df = pd.read_csv('result/test_Ptest.csv', index_col=0)
    pd.concat([PT_df, Ptest_df_post]).to_csv('result/test_Ptest.csv')