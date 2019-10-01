from psychopy import core, visual, event, sound
import pandas as pd

def display_ratingscale(win, text):
    ratingScale = visual.RatingScale(
        win, low=-1, high=1, labels=[u'左', u'どちらも', u'右'], scale=False, pos=(0.0, -100),
        showValue=False, acceptPreText=u'バーをクリック', acceptText='OK')
    while ratingScale.noResponse:
        text.draw()
        ratingScale.draw()
        win.flip()
    return ratingScale.getRating()

def flandars_proc(win):
    inst_textList = [u'文字を書く時、ペンをどちらの手で持ちますか。',
                     u'食事の時、スプーンをどちらの手で持ちますか。',
                     u'歯を磨く時、歯ブラシをどちらの手で持ちますか。',
                     u'マッチを擦る時、\nマッチの軸をどちらの手で持ちますか。',
                     u'消しゴムで文字を消す時、\n消しゴムをどちらの手で持って消しますか。',
                     u'縫い物をする時、針をどちらの手で持って使いますか。',
                     u'パンにバターを塗る時、\nナイフをどちらの手で持ちますか。',
                     u'釘を打つ時、カナヅチをどちらの手で持ちますか。',
                     u'りんごの皮をむく時、\n皮むき器をどちらの手で持ちますか。',
                     u'絵を描く時、ペンや筆をどちらの手で持ちますか。']
    
    summary = pd.DataFrame(columns=['ques_num', 'response'])
    for i, text in enumerate(inst_textList):
        handedScore = display_ratingscale(win, visual.TextStim(win, text, height=80, bold=True, pos=(0.0, 100)))
        series = pd.Series([i+1, handedScore], index=summary.columns)
        summary = summary.append(series, ignore_index=True)
    
    return summary

if __name__ == '__main__':
    event.globalKeys.add(key='escape', func=core.quit)

    win = visual.Window(
		size=(1920, 1080), units='pix', fullscr=True, allowGUI=False)
    
    print(flandars_proc(win))