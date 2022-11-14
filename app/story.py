#Checks for login values avalible in the sqlite3 db
import sqlite3

#PROBLEM how to send varible to another file

def create_story(title, content, user_id):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("SELECT * FROM full_stories")
    story_id_value = len(c.fetchall()) #Creates id based on existing amounts of values in database
    c.execute("INSERT INTO full_stories VALUES(?, ?, ?, ?)", (title, content, story_id_value, content))
    
    
    c.execute("CREATE TABLE IF NOT EXISTS partial_stories(userId INTEGER, storyId INTEGER, addition_content TEXT, sequenceId INTEGER)")
    #c.execute("SELECT * FROM partial_stories WHERE storyId = ?", (story_id_value))
    #sequence_id_value = len(c.fetchall())
    sequence_id_value = 0
    c.execute("INSERT INTO partial_stories VALUES(?, ?, ?, ?)", (user_id, story_id_value, content, sequence_id_value))
	#c.execute("SELECT * FROM logins")
	#pprint(c.fetchall()) #testing
    db.commit()
    db.close()

def story_conflict(title):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("SELECT * FROM full_stories")
    all_stories = c.fetchall()
    for row in all_stories:
        if row[0] == title:
            return True
    return False

def view_stories():
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("SELECT * FROM full_stories")
    return c.fetchall()

#looks through partial_stories table to find which stories a user has edited
#output is a list of tuples, 
#with each tuple containing a storyId of a story the user has contributed to
def find_my_stories(user_id):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS partial_stories(userId INTEGER, storyId INTEGER, addition_content TEXT, sequenceId INTEGER)")
    c.execute("SELECT storyId FROM partial_stories WHERE userId = ?", (str(user_id)))
    my_stories = c.fetchall() 
    print(my_stories)
    return my_stories
 
#returns a list of tuples that contain the title and story content based on a list of 
#storyId tuples
def storyIds_to_title_and_story_content(storyId_list):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    #execute_string = "SELECT title, story_content FROM full_stories WHERE"
    result = [] #a list of tuples containing the title and story content 
    for story_id in storyId_list:
        print(story_id[0])
        #c.execute("SELECT title, story_content FROM full_stories WHERE storyId = ?", (story_id))
        #print(c.fetchall())
        c.execute("SELECT title, story_content FROM full_stories WHERE storyId = ?", (story_id))
        result += c.fetchall()
        #print(result)
    return result
    
    
#NEW AND UNTESTED below -------------------------------------------------------------------
#gets corresponding title to a storyId  
def storyId_to_title(story_id):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("SELECT title FROM full_stories WHERE storyId = ?", (story_id))
    title = c.fetchall[0][0]
    return title
 
#gets corresponding most recent addition to a storyId   
def storyId_to_most_recent_addition(story_id):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("SELECT most_recent_addition FROM full_stories WHERE storyId = ?", (story_id))
    most_recent_addition = c.fetchall[0][0]
    return most_recent_addition

#gets corresponding full story content to a storyId   
def storyId_to_full_content(story_id):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("SELECT story_content FROM full_stories WHERE storyId = ?", (story_id))
    full_content = c.fetchall[0][0]
    return full_content

#updates the full_stories table after somebody has added content
def update_full_story(story_id, added_content):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    full_content = storyId_to_full_content(story_id)
    full_content += ' ' + added_content
    c.execute("UPDATE full_stories SET story_content = ? WHERE storyId = ?", (full_content, story_id))
    db.commit()
    db.close()

#updates partial_stories table when an addition is made to a story
def update_partial_stories(story_id, added_content, user_id):
    db = sqlite3.connect('login.db')
    c  = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS partial_stories(userId INTEGER, storyId INTEGER, addition_content TEXT, sequenceId INTEGER)")
    c.execute("SELECT * FROM partial_stories WHERE storyId = ?", (story_id))
    sequence_index = len(c.fetchall())
    c.execute("INSERT INTO partial_stories VALUES(?, ?, ?, ?)", (user_id, story_id, added_content, sequence_index))
    db.commit()
    db.close()

# updates the full_stories table AND partial_stories table after somebody has added content  
def add_to_story(story_id, added_content, user_id):
    update_full_story(story_id, added_content)
    update_partial_stories(story_id, added_content, user_id)