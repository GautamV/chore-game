import os
import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if __name__ == "__main__":

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
	queries = []

	queries.append("""create table chores (id serial primary key not null,
									chore_name varchar(200) unique not null);""")

	queries.append("""create table users (id serial primary key not null,
									user_name varchar(200) not null,
									phone varchar(20) unique not null);""")

	queries.append("""create table instances (user_id integer not null,
									 		chore_id integer not null,
											timestamp timestamptz not null);""")

	for query in queries: 
		cur.execute(query)