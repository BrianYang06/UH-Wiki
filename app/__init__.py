from flask import Flask, render_template, session, request, redirect, url_for
import os #DONT USE OS BC SLOW for calling files
import login #login.py
import signup #signup.py

the_username = "verit" #Temp user bc we dont have a db set up
the_password = "getstitches"

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def landing_page():
	if 'username' in session:
		return redirect(url_for('home_page'))
	else:
		return render_template("landing_page.html")

@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.route("/login", methods = ['GET', 'POST'])
def login_page():
    if request.method == 'POST': #if after submitting a user and pass through login form
	#	if (os.system(f"login.py {request.form['username']"}  {request.form['password']}))
        if (the_username == request.form['username'] and the_password == request.form['password']): #if user and pass correct
            session['username'] = request.form['username'] #save username to session
            return redirect(url_for('landing_page')) #redirect to welcome
        else:  #user or pass are wrong
            wrongdoings = ''
            if request.form['username'] != the_username:
                wrongdoings += 'User not found, please try again'
            elif request.form['password'] != the_password:
                wrongdoings += 'Incorrect password, please try again'
            return render_template('login.html', authentication_message = wrongdoings)
    else: #accessed login page not from submitting login form
        if 'username' in session: #if already logged in
            return redirect(url_for('home_page')) #no logging in a second time!!
        else:  #not logged in
            return render_template('login.html', authentication_message = '') #go for it!

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('landing_page'))

@app.route("/signup", methods = ['GET', 'POST'])
def signup_page():
	session.pop('username', None)#Just in case they somehow circumnavigate being logged in and trying to sign up
	if request.method == 'POST':
		if len(request.form['username']) == 0 or len(request.form['password']) == 0: #change conditionals to check if it is int db
			return render_template("signup.html", authentication_message = "FAILURE")
		else:
			signup.main(request.form['username'], request.form['password'])
		        #os.system(f"py login.py {request.form['username']} {request.form['password']}")
			return render_template("signup.html", authentication_message = "success")
	return render_template("signup.html")

if __name__ == "__main__":
    app.debug = True #Remove when finished with the project
    app.run()
