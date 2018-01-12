import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

colors = ['b', 'g', 'y', 'c', 'm', 'y', 'k', 'w']

def make_chore_plot(chore, user_data, filepath):
	data = zip(*user_data)
	users = data[0]
	scores = data[1]

	fig = plt.figure()

	y_pos = np.arange(len(users))

	plt.bar(y_pos, scores, align='center', alpha=0.5)
	plt.xticks(y_pos, users)
	plt.ylabel('Times Done')
	plt.title('Stats for {0}'.format(chore))

	fig.savefig(filepath, dpi=fig.dpi)

def make_chores_plot(user_data, filepath):
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
	bar_width = 1.0 / (len(chore_names) * len(user_names))
	opacity = 0.8

	for i, user in enumerate(user_stats): 
		plt.bar(index + i*bar_width, user_stats[user], bar_width,
				alpha=opacity,
				color=colors[i],
				label=user)

	plt.xlabel('Person')
	plt.ylabel('Times Done')
	plt.title('Stats by Chore')
	plt.xticks(index + 0.5*bar_width*(len(user_names) - 1), chore_names)
	plt.legend()
	 
	plt.tight_layout()
	
	fig.savefig(filepath, dpi=fig.dpi)