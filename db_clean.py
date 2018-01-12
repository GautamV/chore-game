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

	cur.execute("""truncate users, chores, instances restart identity;""")