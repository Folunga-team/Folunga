import os
from folunga.models import Profile, Story, friendship
from folunga import db, bcrypt, mail, app
# from folunga.routes import index, reset_password, reset_password_with_token
from flask import jsonify, session, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.utils import secure_filename
import requests


def login(username, password):
    user_account = Profile.query.filter_by(username = username).first()
    if user_account is None:
        return jsonify({'error' : "You have mistyped your username"})

    if not user_account.user_confirmed:
        return jsonify({'error' : "Account not confirmed"})

    if not bcrypt.check_password_hash(user_account.password, password):
        flash("Wrong Password", "error")
        return jsonify({'error' : "Wrong Password! Bad boy, dont try to login to other's accounts"})

    session['id'] = user_account.id
    session['username'] = user_account.username
    session['email'] = user_account.email
    session['password'] = user_account.password
    session['first_name'] = user_account.first_name
    session['last_name'] = user_account.last_name
    session['date_birth'] = user_account.date_birth
    flash("Successful login","success")
    return jsonify({'success' : 'Successful login!'})


def register(new_profile, photo_profile):
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
        filename_photo = secure_filename(photo_profile.filename)
        photo_profile.save(os.path.join(app.config['UPLOAD_FOLDER'], new_profile.username + "." + photo_profile.filename.split(".")[1]))

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


def reset_password(user, password1,password2):
    if password2 == password1:
        hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Password has been reset. Please login", "info")
        return redirect(url_for('index'))
    else:
        flash("Passwords do not match","error")
        return render_template('reset_password.html', title='Reset Password')


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

#--------------------------------------------------Profile Page--------------------------------------------------------------------------
#Displaying profile page and its helper function


def show_profile(username):
    return redirect(url_for('user', username = username))


#--------------------------------------------------Friends---------------------------------------------------------------------------

def list_all_friend_stories():
    all_stories = []
    id_friends = get_id_friends()
    id_friends.append(session['id'])

    for id_f in id_friends:
        story_friend = list(db.engine.execute("SELECT * FROM Story WHERE user_id = :val", {'val':id_f}))
 
        if (isinstance(story_friend, list)):
            for single_story in story_friend:
                all_stories.append(single_story)
        else:
            all_stories.append(story_friend)
            
    return all_stories


#--------------------------------------------------Make New Friends------------------------------------------------------------------
def get_id_friends():
	result = db.engine.execute("SELECT user_first_id FROM friendship WHERE user_second_id = :val", {'val':session['id']})
	list_of_ids1 = [row[0] for row in result]
	result = db.engine.execute("SELECT user_second_id FROM friendship WHERE user_first_id = :val", {'val':session['id']})
	list_of_ids2 = [row[0] for row in result]

	return list_of_ids1 + list_of_ids2

def add_friend(new_friend_id):
	new_relashionship = friendship(user_first_id = session['id'], user_second_id = new_friend_id)
	db.session.add(new_relashionship)
	db.session.commit()

	return jsonify({'success' : "New friend added!"})