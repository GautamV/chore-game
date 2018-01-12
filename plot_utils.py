import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

colors = ['b', 'g', 'y', 'c', 'm', 'y', 'k', 'w']

def make_chore_plot(chore, user_data, filepath, days=None):
	print "making single chore plot"

	data = zip(*user_data)
	users = data[0]
	scores = data[1]

	fig = plt.figure()

	y_pos = np.arange(len(users))
	y_tix = range(0, max(scores) + 1)

	plt.bar(y_pos, scores, align='center', alpha=0.5)
	plt.xticks(y_pos, users)
	plt.yticks(y_tix)
	plt.ylabel('Times Done')
	title = 'Stats for {0} for'.format(chore)
	if days is not None: 
		title += ' Past {0} Days'.format(days)
	else: 
		title += ' All Time'
	plt.title(title)

	print "saving fig"
	fig.savefig(filepath, dpi=fig.dpi)

def make_chores_plot(user_data, filepath, days=None):
	print "making plot for all chores"

	data = zip(*user_data)
	chore_names = list(set(data[1]))
	user_names = list(set(data[0]))
	if len(user_names) > len(colors): 
		user_names = user_names[:len(colors)]

	user_stats = {}
	for name in user_names: 
		user_stats[name] = [0]*len(chore_names)

	for row in user_data:
		user_stats[row[0]][chore_names.index(row[1])] = row[2]
	 
	fig, ax = plt.subplots()
	index = np.arange(len(chore_names))
	bar_width = 0.9 / len(user_names)
	opacity = 0.8

	for i, user in enumerate(user_stats): 
		plt.bar(index + i*bar_width, user_stats[user], bar_width,
				alpha=opacity,
				color=colors[i],
				label=user)

	y_tix = range(0, max([max(i) for i in user_stats.itervalues()]) + 1)

	plt.xlabel('Chore')
	plt.ylabel('Times Done')
	title = 'Stats by Chore for'
	if days is not None: 
		title += ' Past {0} Days'.format(days)
	else: 
		title += ' All Time'
	plt.title(title)
	plt.xticks(index + 0.5*bar_width*(len(user_names) - 1), chore_names)
	plt.yticks(y_tix)
	plt.legend()
	 
	plt.tight_layout()
	
	print "saving fig"
	fig.savefig(filepath, dpi=fig.dpi)