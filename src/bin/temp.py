#!/usr/bin/python3
import sys
import postgresql.driver as pg_driver

"""
db = pg_driver.connect(
	user = 'admin',
	password = '7fadf353697e41b7f8552ccd13f4a9153d13753716a7f2ce46778fe70c3bb6d1b97980ede797d245646a14473126e6d8',
	host = '127.0.0.1',
	port = 5432,
	database = 'kas_dev'
	)
"""

C = pg_driver.default.ip4(
	user = 'admin',
	password = '7fadf353697e41b7f8552ccd13f4a9153d13753716a7f2ce46778fe70c3bb6d1b97980ede797d245646a14473126e6d8',
	host = '127.0.0.1',
	port = 5432,
	database = 'kas_dev'
	)
db = C()
db.connect()


#db.execute('DECLARE the_cursor_id CURSOR WITH HOLD FOR SELECT login FROM person WHERE id=20909;')
db.execute('DECLARE the_cursor_id CURSOR WITH HOLD FOR SELECT 1::text;')
cursor = db.cursor_from_id('the_cursor_id')
assert (cursor.read()[0][0] == '1')

#print (cursor.read())
cursor.close()

sys.exit(0)


rows = db.prepare('SELECT id, environment_name, aws_account_number FROM environment WHERE (deleted IS NOT NULL AND deleted=0) OR deleted IS NULL;')
for row in rows:
	if(row[0] == '' or row[0] is None):
		print ('bad_data - id: %s, name: %s' % (row[0], row[1]))
	else:
		pass
		# print ('row: ', row[2])



sys.exit(0)
