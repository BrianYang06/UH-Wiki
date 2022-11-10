#Checks for login values avalible in the sqlite3 db
import sqlite3

#PROBLEM how to send varible to another file

def add_story(title, content):
	db = sqlite3.connect('login.db')
	c  = db.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER)")
	c.execute("SELECT * FROM full_stories")
	idvalue = len(c.fetchall()) #Creates id based on existing amounts of values in database
	c.execute("INSERT INTO full_stories VALUES(?, ?, ?)", (title, content, idvalue))
	#c.execute("SELECT * FROM logins")
	#pprint(c.fetchall()) #testing
	db.commit()
	db.close()

def view_stories():
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("SELECT * FROM full_stories")
    return c.fetchall()
