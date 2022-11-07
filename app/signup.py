import sqlite3
from pprint import pprint #for testing by printing db
import sys

#for command line argument

def main(user, passw):
	db = sqlite3.connect('login.db')
	c  = db.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
	c.execute("SELECT * FROM logins")
	idvalue = len(c.fetchall())
	c.execute("INSERT INTO logins VALUES(?, ?, ?)", (user, passw, idvalue))
	#c.execute("SELECT * FROM logins")
	#pprint(c.fetchall()) #testing
	db.commit()
	db.close()
