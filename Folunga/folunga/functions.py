from folunga.models import Profile, Story
from folunga import db, bcrypt, mail, app
# from folunga.routes import index, reset_password, reset_password_with_token
from flask import jsonify, session, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests


def login(username, password):
    user_account = Profile.query.filter_by(username = username).first()
    if user_account is None:
        return jsonify({'error' : "You have mistyped your username"})

    if not user_account.user_confirmed:
        return jsonify({'error' : "Account not confirmed"})

    if not bcrypt.check_password_hash(user_account.password, password):
        return jsonify({'error' : "Wrong Password! Bad boy, dont try to login to other's accounts"})

    session['username'] = user_account.username
    session['email'] = user_account.email
    session['password'] = user_account.password
    session['first_name'] = user_account.first_name
    session['last_name'] = user_account.last_name
    session['date_birth'] = user_account.date_birth
    return jsonify({'success' : 'Successful login!'})


def register(new_profile):
    # db.create_all()
    user_exists = Profile.query.filter_by(username = new_profile.username).first()
    email_exists = Profile.query.filter_by(email = new_profile.email).first()

    if user_exists:
        return jsonify({'error' : "Username already used"})
    if email_exists:
        return jsonify({'error' : "Email already used"})

    response = requests.get("https://isitarealemail.com/api/email/validate",
                            params = {'email': new_profile.email})

    status = response.json()['status']
    if status == "valid":
        db.session.add(new_profile)
        db.session.commit()
        token = get_token(new_profile)
        email_subject = "Account Creation"
        email_body = f'''Click the following link to confirm your account
        {url_for('index_after_confirmation', token=token, _external=True)}

        If you did not expect this email then good day. I said good day!
        '''
        send_email(new_profile, email_subject, email_body, token)
    else:
        return jsonify({'error' : "Please Use a Real Email Address"})

    return jsonify({'success' : "We've sent you a confirmation email."})


def confirm_account(user):
    user.user_confirmed = True
    db.session.commit()


def get_token(user, expire_sec=1800):
    s = Serializer(app.secret_key, expire_sec)
    return s.dumps({'user_id': user.id}).decode('utf-8')


def verify_token(token):
    s = Serializer(app.secret_key)
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return Profile.query.get(user_id)


def send_email(user, email_subject, email_body="", token=""):
    msg = Message(email_subject, sender='noreply@folunga.com',
                    recipients=[user.email])
    msg.body = email_body
    mail.send(msg)


def forgot_password(email):
    user = Profile.query.filter_by(email = email).first()
    if user:
        token = get_token(user)
        email_subject = "Forgot Password"
        email_body = f'''To reset your password, visit the following link:
        {url_for('reset_password_with_token', token=token, _external=True)}
        If you did not expect this email then good day. I said good day!
        '''
        send_email(user, email_subject, email_body, token)
        flash("Instructions has been sent to your email", 'info')
        return jsonify({'success' : "Reset your password from the email we've sent you"})
    else:
        return jsonify({'error' : "No username with that email address"})


def reset_password(user, password1, password2):
    if password2 == password1:
        hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Password has been reset. Please login", "info")
        return redirect(url_for('index'))
    else:
        return jsonify({'error' : 'Passwords do not match'})


def remove_non_confirmed_accounts():
    # useless_accounts = Profile.query.filter_by(user_confirmed=False)
    # delete_useless_accounts = Profile.__table__.delete().where(user_confirmed==False)
    # db.session.execute(delete_useless_accounts)
    db.session.query(Profile).filter_by(user_confirmed=False).delete()
    db.session.commit()


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


