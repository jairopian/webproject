import os
import flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_required,
    current_user,
    login_user,
    logout_user,
    LoginManager,
    UserMixin,
)
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from flask_login import UserMixin

db = SQLAlchemy(app)

class UserModel(UserMixin, db.Model):
    """Makes database to save user login"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        """ generates hash for password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """checks password hash"""
        return check_password_hash(self.password_hash, password)


db.create_all()

images=["static/mac.jpg"]
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
	return UserModel.query.get(user_name)

@app.route('/')
def main():
	return flask.redirect(flask.url_for('index'))

@app.route('/index')
def index():
	return flask.render_template(
    	"index.html",
    )

@app.route("/login", methods=["POST", "GET"])
def login():
    """Routes user to login"""
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        user = UserModel.query.filter_by(username=username).first()
        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            return redirect("/membership")
        if user is None:
            flask.flash("Invalid username or password, please try again.")
            return redirect("/login")

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Routes user to sign up page"""
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if UserModel.query.filter_by( username=username).first():
            return "Email already Present"

        user = UserModel(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    """logouts user"""
    logout_user()
    return redirect("/index")

@app.route("/aboutus")
def aboutus():
    return flask.render_template("aboutus.html")

@app.route("/checklist")
def checklist():
    return flask.render_template("checklist.html")

@app.route("/site")
def site():
    return flask.render_template("site.html")


@app.route('/index2')
def index2():
	return flask.render_template(
    	"index2.html",
    )
@app.route("/aboutus2")
def aboutus2():
    return flask.render_template("aboutus2.html")

@app.route("/checklist2")
def checklist2():
    return flask.render_template("checklist2.html")

@app.route("/site2")
def site2():
    return flask.render_template("site2.html")



@app.route("/membership")
@login_required
def membership():
    return render_template(
    "membership.html",
    username=current_user.username)

@app.route('/memberships')
def memberships():
	if current_user.is_authenticated:
		return flask.redirect(flask.url_for('membership'))
	return flask.redirect(flask.url_for('login'))



app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)

