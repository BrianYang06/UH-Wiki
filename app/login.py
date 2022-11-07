import sqlite3
from pprint import pprint
import sys

db = sqlite3.connect('login.db')
c  = db.cursor()

#for command line arguments



#testing additions
#c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
#c.execute("INSERT INTO logins VALUES(?, ?,?)", ("jim", "jimothy", 1))
#c.execute("SELECT * FROM logins")
#print(c.fetchall())

def main(user, passw):
	c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
	c.execute("SELECT * FROM logins")
	idvalue = len(c.fetchall())
	c.execute("INSERT INTO logins VALUES(?, ?, ?)", (user, passw, idvalue))
	c.execute("SELECT * FROM logins")
	pprint(c.fetchall())



if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])

db.commit()
db.close()
