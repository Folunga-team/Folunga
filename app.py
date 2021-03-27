from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates',  static_url_path='',static_folder="static",)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///folunga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# this is for the session
app.secret_key = "folubeautiful" 
CORS(app)

#--------------------------------------------------Class Definitions--------------------------------------------------------------------------

# Class-Profile henceforth shall be declared as a legitimate child of db.Model
# It shall kontain the following attributes: {username, first_name, last_name, email, password, date_birth}
# 2021-03-21 21:59 Dear, Santiago please fix the issue of DateTime attribute
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	
	first_name = db.Column(db.String(20), nullable=False)
	last_name = db.Column(db.String(20), nullable=False)
	
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	
	#date_birth = db.Column(db.DateTime, nullable=False)  
	date_birth = db.Column(db.String(20), nullable=False)  
	profile_pic = db.Column(db.String(50), nullable=False, default='default.jpg')
	
	
	stories = db.relationship('Story', backref='author', lazy=True)
	
	
	def __repr__(self):
		return f"User('{self.username}', '{self.password}')"

	

class Story(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#title = db.Column(db.String(120), nullable=False)
	time = db.Column(db.DateTime, nullable=False)      
	user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
	text = db.Column(db.String(1000), nullable=False)
	
	def __repr__(self):
		return f"Story('{self.text}', '{self.date_posted}'"

class Friendship(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	user_first_id = db.Column(db.String(20), nullable=False)
	user_second_id = db.Column(db.String(20), nullable=False)
	
	
	def __repr__(self):
		return f"Friendship('{self.user_first_id}', '{self.user_second_id}')"

#--------------------------------------------------Messenger--------------------------------------------------------------------------
# Mister Rohan Kola shall develop his messenger system here
@app.route('/message')
def message():
	return display_error("Message page is still under konstruction!")
	
#--------------------------------------------------Story--------------------------------------------------------------------------
def add_story(text):
	story = Story(time = datetime.now(), user_id = id_user_logged, text = text)
	db.session.add(story)
	db.session.commit()
	
	
	
class PrintableStory:
	def __init__(self, other):
		self.name = full_name(other.author)
		self.time = other.time.strftime("%d.%m.%Y %H:%M:%S")
		self.text = other.text

def make_printable(lst_raw):
	lst_print = []
	for raw_story in lst_raw:
		lst_print.append(PrintableStory(raw_story))
	
	return lst_print

#Here I return a list of stories that can be mre easily displayed on the folunga.com/user page	
def printable_stories_person(profile):
	lst_print = profile.stories
	
	return make_printable(lst_print)

def printable_stories(lst_profiles):
	lst_print = []
	for profile in lst_profiles:
		lst_print.extend(printable_stories_person(profile))
	
	return lst_print

# currently i use all stories, but they must be changed in the deep futre of time
def printable_stories_all():
	lst_print = Story.query.all()
	return make_printable(lst_print)

#--------------------------------------------------Profile Page--------------------------------------------------------------------------
#Displaying profile page and its helper function
@app.route('/user/<username>', methods = ['GET', 'POST'])
def user(username):
	human = Profile.query.filter_by(username=username).first()
	
	if human is None:
		return display_error("Invalid username, this user does not exist")
		
	return render_template('user.html')
	
def show_profile(username):
	return redirect(url_for('user', username = username))

#--------------------------------------------------Feed Page--------------------------------------------------------------------------
#Displays all user's stories
@app.route('/feed', methods = ['GET', 'POST'])
def feed():
	return render_template('feed.html')

#--------------------------------------------------Make New Friends---------------------------------------------------------------------------

#This displays a page where you can see all profiles from Folunga that are not your friends
@app.route('/make_new_friends', methods = ['GET', 'POST'])
def make_new_friends():
	if request.method == 'POST':
		return add_friend(request.form['new_friend_id'])
	
	all_friends = get_id_friends()
	#because we don't want to see our profile
	all_friends.append(session['id'])
            
	return render_template('make_new_friends.html',  users = Profile.query.filter(Profile.id.notin_(all_friends)).all())

def get_id_friends():
	result = db.engine.execute("SELECT user_first_id FROM Friendship WHERE user_second_id = :val", {'val':session['id']})
	list_of_ids1 = [row[0] for row in result]
	result = db.engine.execute("SELECT user_second_id FROM Friendship WHERE user_first_id = :val", {'val':session['id']})
	list_of_ids2 = [row[0] for row in result]

	return list_of_ids1 + list_of_ids2

def add_friend(new_friend_id):
	new_relashionship = Friendship(user_first_id = session['id'], user_second_id = new_friend_id)
	db.session.add(new_relashionship)
	db.session.commit()

	return jsonify({'success' : "New friend added!"})

#--------------------------------------------------Friends---------------------------------------------------------------------------

@app.route('/friends')
def friends():
	
	all_friends = get_id_friends()
            
	return render_template('friends.html',  list_friends = Profile.query.filter(Profile.id.in_(all_friends)).all())



# This is the index page, where the user can login, register or reset-pass.
# (.) If the user is already logged(we verify it with sessions) -> we redirect him/her to feed
# (.) If we receive a POST request from the client side -> 
#		That means that the user wants to register or log in or reset pw
@app.route('/', methods = ['GET', 'POST'])
def index():
    if 'username' in session:
        	return redirect(url_for('user', username = session['username']))
    if request.method == 'POST':
        if request.form.get('form') == 'login':

            username = request.form['username']
            password = request.form['password']
            return login(username, password)

        elif request.form.get('form') == 'registration':
            new_profile = Profile()
            new_profile.username = request.form['username']
            new_profile.first_name = request.form['first_name']
            new_profile.last_name = request.form['last_name']
            new_profile.email = request.form['email']
            new_profile.password = request.form['password']
            new_profile.date_birth = request.form['date_birth']
            password2 = request.form['password2']
            
            return register(new_profile, password2)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

# Here we verify if all the data recived from the user is correct. 
# (.) If it is correct -> we create a session with the data of the user and send a success message to the client side.
# (.) If it is incorrect -> we send I error message to the client side.
def login(username, password):
	user_account = Profile.query.filter_by(username = username).first()
	
	if user_account is None:
		return jsonify({'error' : "You have mistyped your username"})
	
	if user_account.password != password:
		return jsonify({'error' : "Wrong Password! Bad boy, dont try to login to other's accounts"})
	
	session['id'] = user_account.id
	session['username'] = user_account.username
	session['email'] = user_account.email
	session['password'] = user_account.password
	session['first_name'] = user_account.first_name
	session['last_name'] = user_account.last_name
	session['date_birth'] = user_account.date_birth
	return jsonify({'success' : 'Successful login!'})

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

# Here we verify if all the data recived from the user is correct.
# (.) If it is correct -> we upload the data to the db and send a success message to the client side.
# (.) If it is incorrect -> we send I error message to the client side.
def register(new_profile, password2):
	user_exists = Profile.query.filter_by(username = new_profile.username).first()
	email_exists = Profile.query.filter_by(email = new_profile.email).first()
	
	if user_exists:
		return jsonify({'error' : "Username already used"})
	if email_exists:
		return jsonify({'error' : "Email already used"})
	if password2 != new_profile.password:
		return jsonify({'error' : "Passwords are different"})
	
	db.session.add(new_profile)
	db.session.commit()
	return jsonify({'success' : "Account created! We've sent you a confirmation email."})

		
if __name__ == '__main__':
	app.run(debug=True)
	db.create_all()