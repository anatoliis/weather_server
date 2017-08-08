import sqlite3


db_connection = sqlite3.connect('weather01.db')
cur = db_connection.cursor()

cur.execute('UPDATE weather SET tc = 30 WHERE tc = -273')
db_connection.commit()

cur.execute('SELECT count(*) FROM weather WHERE tc = 30')
result = cur.fetchone()

cur.close()
print(result)
