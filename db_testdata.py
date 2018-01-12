import db_utils

users = [('Gautam', '+19084204948'), ('Shyam', '+19083589340'), ('Shravan', '+19083589574')]
chores = ['Dishes', 'Cleaning', 'Laundry']
instances = [(1, 1), (1, 2), (2, 1), (2, 3), (1, 1, 14), (2, 3, 14)]

for user in users:
	db_utils.add_user(user)

for chore in chores:
	db_utils.add_chore(chore)

for instance in instances:
	db_utils.add_instance(instance)