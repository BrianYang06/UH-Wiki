from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

if __name__ == "__main__":
    app.debug = True #Remove when finished with the project
    app.run()
