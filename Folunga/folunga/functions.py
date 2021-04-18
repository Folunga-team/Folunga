from folunga.models import Profile, Story
from folunga import db
from flask import jsonify, session


def login(username, password):
    print(username, password)
    user_account = Profile.query.filter_by(username = username).first()

    if user_account is None:
        return jsonify({'error' : "You have mistyped your username"})

    if user_account.password != password:
        return jsonify({'error' : "Wrong Password! Bad boy, dont try to login to other's accounts"})

    session['username'] = user_account.username
    session['email'] = user_account.email
    session['password'] = user_account.password
    session['first_name'] = user_account.first_name
    session['last_name'] = user_account.last_name
    session['date_birth'] = user_account.date_birth
    return jsonify({'success' : 'Successful login!'})



# Here we verify if all the data recived from the user is correct.
# (.) If it is correct -> we upload the data to the db and send a success message to the client side.
# (.) If it is incorrect -> we send I error message to the client side.
def register(new_profile, password2):
    user_exists = Profile.query.filter_by(username = new_profile.username).first()
    email_exists = Profile.query.filter_by(email = new_profile.email).first()

    # if validate_email(new_profile.email) == False:
    #     return jsonify({'error' : "Invalid Email"})
    if user_exists:
        return jsonify({'error' : "Username already used"})
    if email_exists:
        return jsonify({'error' : "Email already used"})
    if password2 != new_profile.password:
        return jsonify({'error' : "Passwords are different"})

    db.session.add(new_profile)
    db.session.commit()
    return jsonify({'success' : "Account created! We've sent you a confirmation email."})
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


def show_profile(username):
    return redirect(url_for('user', username = username))


#--------------------------------------------------Friends---------------------------------------------------------------------------

#This section is completely under developemnt

def friend_list_generator(user_id):
    #THis must be changes soon!!!!!
    return Profile.query.all()


def inject_friend_list(whom, lst):
    return render_template('friends.html',  logged_in = check_log(), profile = logged_user(), whom = whom, lst_profiles = lst)

#This displays a page where you can see the list of all people on Folunga

# This needs development from the database system




# This is the index page, where the user can login, register or reset-pass.
# (.) If the user is already logged(we verify it with sessions) -> we redirect him/her to feed
# (.) If we receive a POST request from the client side ->
#       That means that the user wants to register or log in or reset pw


# Here we verify if all the data recived from the user is correct.
# (.) If it is correct -> we create a session with the data of the user and send a success message to the client side.
# (.) If it is incorrect -> we send I error message to the client side.

