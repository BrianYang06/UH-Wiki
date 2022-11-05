import sqlite3
import pprint
import sys

db = sqlite3.connect('login.db')
c  = db.cursor()

#for command line arguments
#user = sys.argv[0]
#passw = sys.argv[1]

#testing additions
#c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
#c.execute("INSERT INTO logins VALUES(?, ?,?)", ("jim", "jimothy", 1)) 
#c.execute("SELECT * FROM logins")
#print(c.fetchall())

#def main(user, passw):
c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
c.execute("SELECT * FROM logins")
idvalue = len(c.fetchall())
c.execute("INSERT INTO logins VALUES(?, ?, ?)", ("joe", "joey", idvalue))
c.execute("SELECT * FROM logins")
print(c.fetchall())



#if __name__ == "__main__":


db.commit()
db.close()
