from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

class Profile:
	username = "def_username"
	name = "def_name"
	email = "def_email"
	password = "def_password"
	num_likes = 0;
	

lst_profiles = []
def check_find_username(username):
	i = 0
	for profile in lst_profiles:
		if username == profile.username:
			return i
		i += 1
	return -1

#Error message, and its helper function
@app.route('/error_message/<message>')
def error_message(message):
	return render_template('error_message.html', message = message)
	
def display_error(message):
	return redirect(url_for('error_message', message = message))


#Displaying profile page and its helper function
@app.route('/profile_page/<username>', methods = ['GET', 'POST'])
def profile_page(username):
	location = check_find_username(username)
		
	if request.method == 'POST':
		lst_profiles[location].num_likes += 1
		
	elif location == -1:
		return display_error("Invalid username, this user does not exist")	
	
	return render_template('profile_page.html', profile = lst_profiles[location])
		
def show_profile(username):
	return redirect(url_for('profile_page', username = username))


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		return redirect(url_for('login', username = username, password = password))
	else:
		return render_template('index.html')


@app.route('/login/<username>/<password>')
def login(username, password):
	location = check_find_username(username)
	
	if location == -1:
		return display_error("You have mistyped your username")
		
	if password != lst_profiles[location].password:
		return display_error("Wrong Password! Bad boy, dont try to login to other's accounts")
		
	return show_profile(username)


@app.route('/all_profiles')
def all_profiles():
	return render_template("all_profiles.html", lst_profiles = lst_profiles, num_profiles = len(lst_profiles))


@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		profile = Profile()
		profile.username = request.form['username']
		profile.name = request.form['name']
		profile.email = request.form['email']
		profile.password = request.form['password']
		profile.num_likes = 0
		
		lst_profiles.append(profile)
		return redirect(url_for('index'))
		
	else:
		return render_template('registration_page.html')
	

	

if __name__ == '__main__':
	app.run(debug = True)
