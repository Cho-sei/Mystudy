import pandas as pd
import matplotlib.pyplot as plt
import sys

data = pd.read_csv('result/' + sys.argv[1] + '_MR.csv')

for i, hand in enumerate(['left', 'right']):
	plt.subplot(1, 2, i+1)
	pre = data[(data.timing == 'pre') & (data.hand == hand)]
	post = data[(data.timing == 'post') & (data.hand == hand)]
	pre_result = pre['response'].mean() / pre['RT'].mean()
	post_result = post['response'].mean() / post['RT'].mean()
	plt.plot(['pre', 'post'], [0, post_result-pre_result])
	plt.title(hand)
	plt.ylim(0, 0.5)

plt.show()
