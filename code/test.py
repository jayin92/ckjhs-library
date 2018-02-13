import sqlite3
import time
conn = sqlite3.connect('library.db')

def get_data_from_database(table):
	global conn
	c = conn.cursor()
	c.execute("SELECT * FROM "+table)
	rows = c.fetchall()
	return [list(t) for t in rows]
start = time.time()
# print(get_data_from_database('book'))
# bookData  = get_data_from_database('book')
c = conn.cursor()
c.execute("SELECT title FROM book WHERE isbn='9789573249245'")
print(c.fetchall())
print(time.time()-start)
# for item in bookData:
# 	if item[3] == '9789573249245':
# 		print("find!")
# 		print(time.time()-start)
