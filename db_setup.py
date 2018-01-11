import os
import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if __name__ == "__main__":

	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])

	conn = psycopg2.connect(
		database=url.path[1:],
		user=url.username,
		password=url.password,
		host=url.hostname,
		port=url.port
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