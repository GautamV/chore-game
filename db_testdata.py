import db_utils

users = [('Gautam', '+19084204948'), ('Shyam', '+19083589340'), ('Shravan', '+19083589574')]
chores = ['Dishes', 'Cleaning', 'Laundry']
instances = [(1, 1, 0), (1, 2, 0), (2, 1, 0), (2, 3, 0), (1, 1, 14), (2, 3, 14)]

for user in users:
	db_utils.add_user(user[0], user[1])
print "users table:"
print db_utils.get_users()

for chore in chores:
	db_utils.add_chore(chore)
print "chores table:"
print db_utils.get_chores()

for instance in instances:
	db_utils.add_instance(instance[0], instance[1], instance[2])
print "instances table:"
print db_utils.get_instances()