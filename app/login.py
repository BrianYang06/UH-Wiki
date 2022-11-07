#Checks for login values avalible in the sqlite3 db
import sqlite3

#PROBLEM how to send varible to another file

def main(user, passw):
    db = sqlite3.connect('login.db')
    c = db.cursor()
    #check if table exists
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'logins' ''')
    if c.fetchone()[0] == 1:
        c.execute("SELECT * FROM logins")
        list = c.fetchall() #makes the entire db into a list that stores tuples
        for x in list:
            if (x[0] == user) and (x[1] == passw):
                db.close()
                return 1
            else:
                db.close()
                return 0
