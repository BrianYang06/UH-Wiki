#Checks for login values avalible in the sqlite3 db
import sqlite3

#PROBLEM how to send varible to another file

def exist(user, passw):
    db = sqlite3.connect('login.db')
    c = db.cursor()
    #check if table exists
    pass_true = False
    user_true = False
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'logins' ''')
    if c.fetchone()[0] == 1:
        c.execute("SELECT * FROM logins")
        list = c.fetchall() #makes the entire db into a list that stores tuples
        for x in list:
            if (x[0] == user):
                user_true = True
            if (x[1] == passw):
                pass_true = True

    if user_true and pass_true:
        db.close()
        return 1
    elif user_true != True:
        db.close()
        return 'user'
    elif pass_true != True:
        db.close()
        return 'pass'
