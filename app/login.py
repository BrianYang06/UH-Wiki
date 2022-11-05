import sqlite3


db = sqlite3.connect('login.db')
c  = db.cursor()

#testing additions
c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
c.execute("INSERT INTO logins VALUES(?, ?,?)", ("jim", "jimothy", 1)) 
c.execute("SELECT * FROM logins")
print(c.fetchall())

#def main(user, passw):
#	x = login.fetchall()
#	print(type(x))
#	print(x)


#if __name__ == "__main__":
#	main('no', 'no')

db.commit()
db.close()
