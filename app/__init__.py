from flask import Flask, render_template, session, request, redirect, url_for
import os
import login #login.py
import signup #signup.py
import story #create_story.py
import sqlite3

DB_FILE = "discobandit.db"

app = Flask(__name__)
app.secret_key = 'foo'

@app.route("/")
def landing_page():
    if 'username' in session:
        #session.pop('username', None)
        #session.pop('id', None)
        return redirect(url_for('home_page'))
    else:
        return render_template("landing_page.html")

@app.route("/home")
def home_page():
    print(story.storyIds_to_title_and_story_content(story.find_my_stories(session['id'])))
    return render_template("home_page.html", data=story.storyIds_to_title_and_story_content(story.find_my_stories(str(session['id']))))

@app.route("/login", methods = ['GET', 'POST'])
def login_page():
    if request.method == 'POST': #if after submitting a user and pass through login form
        binaryTF = login.exist(request.form['username'], request.form['password'])
        if binaryTF == 1: #if user and pass correct
            session['username'] = request.form['username'] #save username to session
            session['id'] = login.user_to_id(session['username']) #save id
            print(session['username'])
            print(session['id'])
            return redirect(url_for('landing_page')) #redirect to welcome
        elif binaryTF == 'pass':  #user or pass are wrong
            return render_template('login.html', authentication_message = 'Incorrect password, please try again')
        elif binaryTF == 'user':
            return render_template('login.html', authentication_message = 'User not found, please try again')
    else: #accessed login page not from submitting login form
        if 'username' in session: #if already logged in
            return redirect(url_for('home_page')) #no logging in a second time!!
        else:  #not logged in
            return render_template('login.html', authentication_message = '') #go for it!

@app.route('/logout')
def logout():
    session.pop('username', None) # remove the username from the session if it's there
    return redirect(url_for('landing_page'))

@app.route("/signup", methods = ['GET', 'POST'])
def signup_page():
	session.pop('username', None)#Just in case they somehow circumnavigate being logged in and trying to sign up
	if request.method == 'POST':
		problem = signup.check_user_conflict(request.form['username'], request.form['password']) #cycle over types of problems to find what it is
		if  problem == 'user': #change conditionals to check if it is in db
			return render_template("signup.html", authentication_message = "Username taken")
		if problem == 'pass':
			return render_template("signup.html", authentication_message = "Create a longer password")
		elif problem == '1':
			signup.add(request.form['username'], request.form['password'])
		        #os.system(f"py login.py {request.form['username']} {request.form['password']}")
			return render_template("signup.html", authentication_message = "Acount created")
	return render_template("signup.html")

@app.route("/create_story_page", methods = ['GET', 'POST'])
def create_story_page():
	print(session['username'])
	if request.method == 'POST':
		if story.story_conflict(request.form['story_title']):
			return render_template('create_story.html', authentication_message="Title Already Exists")
		else:
			story.create_story(request.form['story_title'],request.form['story_content'],session['id'])
			return render_template('create_story.html', authentication_message="Success!")
	else:
		return render_template('create_story.html', authentication_message="")

@app.route("/view_story_page", methods = ['GET', 'POST'])
def view_story_page():
	return render_template('view_stories.html',data=story.view_stories(session['id']))


###############################################################This is new
#UNDER CONTRUCTION

@app.route("/add_to_story_page", methods = ['GET', 'POST'])
def add_to_story_page():
    #print(request.args)
    #print(list(request.args.keys())[0])
    
    user_id = session['id']
    added_content = ''
    story_title = ''
    
    if request.method == 'POST':       
        added_content = request.form['story_content']
        story.add_to_story(session['story_id'], added_content, user_id)
    else:
        session['story_id']=list(request.args.keys())[0]

    story_title = story.storyId_to_title(session['story_id'])
    story_most_recent = story.storyId_to_most_recent_addition(session['story_id'])
    return render_template('add_to_story.html', title = story_title, last_addition = story_most_recent, \
                           valid_user = story.check_editable(session['id'], session['story_id']))
 

if __name__ == "__main__":
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS full_stories(title TEXT, story_content TEXT, storyId INTEGER, most_recent_addition TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS partial_stories(userId INTEGER, storyId INTEGER, addition_content TEXT, sequenceId INTEGER)")
    
    app.debug = True #Remove when finished with the project
    app.run()
