import flask
from flask_login.utils import login_required
import requests
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


from flask_login import login_user, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
# Point SQLAlchemy to your Heroku database
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from flask_login import UserMixin

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))

	def __repr__(self):
		return f"<User {self.username}>"

	def get_username(self):
		return self.username


db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
	return User.query.get(user_name)

@app.route('/signup')
def signup():
	return flask.render_template("signup.html")

@app.route('/signup', methods=["POST"])
def signup_post():
	username = flask.request.form.get('username')
	user = User.query.filter_by(username=username).first()
	if user:
		pass
	else:
		user = User(username=username)
		db.session.add(user)
		db.session.commit()
	
	return flask.redirect(flask.url_for('login'))

@app.route('/login')
def login():
	return flask.render_template("login.html")

@app.route('/login', methods=["POST"])
def login_post():
	username = flask.request.form.get('username')
	user = User.query.filter_by(username=username).first()
	if user:
		login_user(user)
		return flask.redirect(flask.url_for('index'))

	else:
		return flask.jsonify(
			{"status": 401,"reason": "Username or Password Error"}
		)




@app.route('/')
def main():
	if current_user.is_authenticated:
		return flask.redirect(flask.url_for('index'))
	return flask.redirect(flask.url_for('login'))

@app.route('/index')
@login_required
def index():
	return flask.render_template(
    	"index.html",
    )

if __name__ == "__main__":
	app.run(
		host=os.getenv('IP', '0.0.0.0'),
		port=int(os.getenv('PORT', 8080)),
		debug=True
	)

