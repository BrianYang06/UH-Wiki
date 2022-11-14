import sqlite3
from pprint import pprint #for testing by printing db

def add(user, passw):
	db = sqlite3.connect('login.db')
	c  = db.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
	c.execute("SELECT * FROM logins")
	idvalue = len(c.fetchall()) #Creates id based on existing amounts of values in database
	c.execute("INSERT INTO logins VALUES(?, ?, ?)", (user, passw, idvalue))
	c.execute("SELECT * FROM logins")
	pprint(c.fetchall()) #testing
	db.commit()
	db.close()

def check_user_conflict(user, passw):
	db = sqlite3.connect('login.db')
	c  = db.cursor()
	c.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'logins' ''')
	username = False
	password = False
	if c.fetchone()[0] == 1:
		c.execute("SELECT * FROM logins")
		list = c.fetchall() #makes the entire db into a list that stores tuples
		for usernames in list:
			#print(usernames[0])
			if usernames[0] == user:
				username = True
	if len(passw) < 8:
		password = True

	if username == True:
		db.commit()
		db.close()
		return 'user' #Username is taken
	elif password == True:
		db.commit()
		db.close()
		return 'pass' #Password is too short
	else:
		db.commit()
		db.close()
		return '1' #Gud


def test():
	return True
