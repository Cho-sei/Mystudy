from psychopy import core, visual, event, sound
import itertools
import pandas as pd
from instruction import instruction
from experiment_parameter import MIexperiment_components

def performance_test(win, components, instruction, timing, handed):
    #DataFrame
    trial_proc = ('left', 'right') if handed == 'left' else ('right', 'left')
    conditions = list(itertools.product(
        range(components.PTtrial),
        trial_proc,
    ))
    df = pd.DataFrame(
        conditions, columns=('trial', 'hand'))
    
    clock = core.Clock()

    PTime = []
    for i, row in df.iterrows():
        
        if row['hand'] == 'left':
            sound = 'lefthand'
            components.msg.setText(u'左手')
        else:
            sound = 'righthand'
            components.msg.setText(u'右手')

        components.msg.draw()
        win.flip()

        instruction.PlaySound(sound)

        instruction.PlaySound('PT_start')
        t_start = clock.getTime()
        key = event.waitKeys(keyList=['return'])
        PTime.append(clock.getTime() - t_start)

        if i != len(df)-1:
            components.msg.setText('Ready')
            components.msg.draw()
            win.flip()
            instruction.PlaySound('otsukaresama')
            instruction.PlaySound('move_tenkey')
            event.waitKeys(keyList=['return'])
            instruction.PlaySound('PT_next')

    df['PTime'] = PTime
    df['timing'] = timing

    return df[['timing', 'trial', 'hand', 'PTime']]


if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(units='pix', fullscr=True, allowGUI=False)
    components = MIexperiment_components(win)
    instruction = instruction(win, components)

    Ptest_df = performance_test(win, components, instruction, 'pre', 'right')
    Ptest_df.to_csv('result/test_Ptest.csv')

    Ptest_df_post = performance_test(win, components, instruction, 'post', 'right')
    PT_df = pd.read_csv('result/test_Ptest.csv', index_col=0)
    pd.concat([PT_df, Ptest_df_post]).to_csv('result/test_Ptest.csv')