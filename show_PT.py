import pandas as pd
import matplotlib.pyplot as plt
import sys

data = pd.read_csv('result/' + sys.argv[1] + '_PT.csv')

plt.subplot(1, 2, 1)
pre = data[(data.timing == 'pre') & (data.hand =='left')].PTime.mean()
post = data[(data.timing == 'post') & (data.hand =='left')].PTime.mean()
plt.plot(['pre', 'post'], [0, post-pre])
plt.ylim(-3, 0)
plt.title('left')

plt.subplot(1, 2, 2)
pre = data[(data.timing == 'pre') & (data.hand =='right')].PTime.mean()
post = data[(data.timing == 'post') & (data.hand =='right')].PTime.mean()
plt.plot(['pre', 'post'], [0, post-pre])
plt.ylim(-3, 0)
plt.title('right')

plt.show()