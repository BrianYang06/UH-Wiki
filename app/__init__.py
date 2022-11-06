from flask import Flask, render_template, session, request, redirect, url_for
import os
import login #login.py

the_username = "verit" #Temp user bc we dont have a db set up
the_password = "getstitches"

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.route("/login", methods = ['GET', 'POST'])
def login_page():
    if 'username' in session:
        if session['username'] == the_username and session['password'] == the_password:
            return render_template("home_page.html")
        else:
            # Must highlight what the user did wrong
            wrongdoings=""
            if session['username'] != the_username:
                wrongdoings+=' Username Wrong'
            if session['password'] != the_password:
                wrongdoings+=' Password Wrong'
            return render_template("error.html", huhs=wrongdoings)
    return render_template("login.html")

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    session['username'] = request.form['username']
    session['password'] = request.form['password']
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route("/signup", methods = ['GET', 'POST'])
def signup_page():
    return render_template("signup.html")

@app.route("/signup_response", methods=['GET', 'POST'])
def success():
    if len(request.form['username']) == 0 or len(request.form['password']) == 0: #change conditionals to check if it is int db
        return render_template("signup.html")
    else:
        os.system(f"py login.py {request.form['username']} {request.form['password']}")
        return render_template("signup_success.html")

if __name__ == "__main__":
    app.debug = True #Remove when finished with the project
    app.run()
