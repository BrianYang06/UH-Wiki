#Checks for login values avalible in the sqlite3 db
import sqlite3

DB_FILE = "discobandit.db"

def create_story(title, content, user_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT * FROM full_stories")
    story_id_value = len(c.fetchall()) #Creates id based on existing amounts of values in database
    c.execute("INSERT INTO full_stories VALUES(?, ?, ?, ?)", (title, content, story_id_value, content))
    
    
    #c.execute("SELECT * FROM partial_stories WHERE storyId = ?", (story_id_value))
    #sequence_id_value = len(c.fetchall())
    sequence_id_value = 0
    c.execute("INSERT INTO partial_stories VALUES(?, ?, ?, ?)", (user_id, story_id_value, content, sequence_id_value))
	#c.execute("SELECT * FROM logins")
	#pprint(c.fetchall()) #testing
    db.commit()
    db.close()

def story_conflict(title):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT * FROM full_stories")
    all_stories = c.fetchall()
    for row in all_stories:
        if row[0] == title:
            return True
    return False

#gets stories and data from full_stories table that the user can add to
def view_stories(user_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    my_stories = find_my_stories(user_id) #gets all stories user has contributed to
    print(my_stories)
    c.execute("SELECT * FROM full_stories")
    editable_stories = c.fetchall() 
    #print(editable_stories)
    for story in editable_stories:
        for story_id in my_stories:
            #print(story[2])
            #print(story_id[0])
            if story[2] == story_id[0]: #if user had edited story
                editable_stories.remove(story) #remove it
    #print(editable_stories)
    return editable_stories

#takes in a user_id and story_id and checks if the user is allowed to add to that story
#aka they have never contributed to that story before   
def check_editable(user_id, story_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    my_stories = find_my_stories(user_id)
    #print(my_stories)
    for edited_story_id in my_stories:
        #print('start:')
        #print(type(story_id))
        #print(type(edited_story_id[0]))
        #print(edited_story_id[0] == int(story_id))
        if edited_story_id[0] == int(story_id):            
            #print(False)
            return False
    #print(True)
    return True

#looks through partial_stories table to find which stories a user has edited
#output is a list of tuples, 
#with each tuple containing a storyId of a story the user has contributed to
def find_my_stories(user_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT storyId FROM partial_stories WHERE userId = ?", (str(user_id)))
    my_stories = c.fetchall() 
    print(my_stories)
    return my_stories
 
#returns a list of tuples that contain the title and story content based on a list of 
#storyId tuples
def storyIds_to_title_and_story_content(storyId_list):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
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
       
#gets corresponding title to a storyId  
def storyId_to_title(story_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT title FROM full_stories WHERE storyId = ?", (story_id))
    title = c.fetchall()[0][0] #[(title,)]
    return title
 
#gets corresponding most recent addition to a storyId   
def storyId_to_most_recent_addition(story_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT most_recent_addition FROM full_stories WHERE storyId = ?", (story_id))
    most_recent_addition = c.fetchall()[0][0]
    return most_recent_addition

#gets corresponding full story content to a storyId   
def storyId_to_full_content(story_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT story_content FROM full_stories WHERE storyId = ?", (story_id))
    full_content = c.fetchall()[0][0]
    return full_content

#updates the full_stories table after somebody has added content
def update_full_story(story_id, added_content):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    full_content = storyId_to_full_content(story_id)
    full_content += ' ' + added_content
    c.execute("UPDATE full_stories SET story_content = ? WHERE storyId = ?", (full_content, story_id))
    c.execute("UPDATE full_stories SET most_recent_addition = ? WHERE storyId = ?", (added_content, story_id))
    db.commit()
    db.close()

#updates partial_stories table when an addition is made to a story
def update_partial_stories(story_id, added_content, user_id):
    db = sqlite3.connect(DB_FILE)
    c  = db.cursor()
    c.execute("SELECT * FROM partial_stories WHERE storyId = ?", (story_id))
    sequence_index = len(c.fetchall())
    c.execute("INSERT INTO partial_stories VALUES(?, ?, ?, ?)", (user_id, story_id, added_content, sequence_index))
    db.commit()
    db.close()

# updates the full_stories table AND partial_stories table after somebody has added content  
def add_to_story(story_id, added_content, user_id):
    update_full_story(story_id, added_content)
    update_partial_stories(story_id, added_content, user_id)