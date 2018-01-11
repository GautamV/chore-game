import os
import urlparse
import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# change this for heroku 
conn = psycopg2.connect(
	database='chore_gamev4',
	user='postgres',
	password='pass',
	host='localhost',
	port='5432'
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

min_date = datetime.datetime(year=datetime.MINYEAR, month=1, day=1)
max_date = datetime.datetime(year=datetime.MAXYEAR, month=1, day=1)

user_table = 'users'
chore_table = 'chores'
instance_table = 'instances'

def add_chore(name):
	values = [name]
	q = make_insert_query_default_id(chore_table, values)
	return cur.execute(q, values)

def add_user(name, phone_number):
	values = [name, phone_number]
	q = make_insert_query_default_id(user_table, values)
	return cur.execute(q, values)

def add_instance(user_id, chore_id):
	values = [user_id, chore_id, datetime.datetime.utcnow()]
	q = make_insert_query(instance_table, values)
	return cur.execute(q, values)

def make_insert_query(table_name, values):
	s = "insert into {0} values (".format(table_name)
	for i in xrange(len(values)):
		s += "%s, "

	s = s[:-2]
	s += ")"

	return s

def make_insert_query_default_id(table_name, values):
	s = "insert into {0} values (default, ".format(table_name)
	for i in xrange(len(values)):
		s += "%s, "

	s = s[:-2]
	s += ")"

	return s

def get_naive_stats(start_date=min_date, end_date=max_date):
	q = """
		select user_name, count(*) as count from 
			(select user_name, timestamp from users join instances on users.id = instances.user_id where timestamp >= %s and timestamp <= %s) as users_instances 
		group by user_name;
		"""
	d = [start_date, end_date]
	cur.execute(q, d)

	return cur.fetchall()

def get_chores_stats(start_date=min_date, end_date=max_date):
	q = """
		select user_name, chore_name, count(*) as count from 
			((select user_name, chore_id, timestamp from users join instances on users.id = instances.user_id where timestamp >= %s and timestamp <= %s) as users_instances 
			join chores on users_instances.chore_id = chores.id) as all_data
		group by user_name, chore_name;
		"""
	d = [start_date, end_date]
	cur.execute(q, d)

	return cur.fetchall()

def get_chore_stats(chore_name, start_date=min_date, end_date=max_date):
	q = """
		select user_name, count(*) as count from 
			((select user_name, chore_id, timestamp from users join instances on users.id = instances.user_id where timestamp >= %s and timestamp <= %s) as users_instances 
			join chores on users_instances.chore_id = chores.id) as all_data where chore_name = %s
		group by user_name;
		"""
	d = [start_date, end_date, chore_name]
	cur.execute(q, d)

	return cur.fetchall()

def get_users():
	q = "select * from {0};".format(user_table)
	cur.execute(q)

	return cur.fetchall()

def get_chores():
	q = "select * from {0};".format(chore_table)
	cur.execute(q)

	return cur.fetchall()

def get_instances():
	q = "select * from {0};".format(instance_table)
	cur.execute(q)

	return cur.fetchall()

def get_user_by_phone(number):
	q = "select id, user_name from users where phone = %s;"
	d = [number]
	cur.execute(q, d)

	return cur.fetchone()

def get_chore_id_by_name(chore):
	q = "select id from chores where chore_name = %s;"
	d = [chore]
	cur.execute(q, d)

	return cur.fetchone()