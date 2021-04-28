from flask import render_template, url_for, flash, redirect, request, session, jsonify
from datetime import datetime
from folunga import app, bcrypt
from folunga.forms import LoginForm, RegistrationForm
from folunga.functions import *
from flask_mail import Message

@app.route('/', methods = ['GET', 'POST'])
def index():
    db.create_all()

    if 'username' in session:
            return redirect(url_for('user', username = session['username']))
    if request.method == 'POST':
        if request.form.get('form') == 'login':

            username = request.form['username']
            password = request.form['password']
            return login(username, password)

        elif request.form.get('form') == 'registration':
            new_profile = Profile()
            new_profile.username = request.form['username_registration']
            new_profile.first_name = request.form['first_name']
            new_profile.last_name = request.form['last_name']
            new_profile.email = request.form['email_registration']
            new_profile.date_birth = request.form['date_birth']
            photo_profile = request.files['photo_registration']

            if request.form['password_registration'] != request.form['password2_registration']:
                return jsonify({'error' : "Passwords do not match"})
            hashed_password = bcrypt.generate_password_hash(request.form['password_registration']).decode('utf-8')
            new_profile.password = hashed_password
            return register(new_profile, photo_profile)

        elif request.form.get('form') == 'recovery_password':
            return forgot_password(request.form["email_recovery"])

    else:
        # remove_non_confirmed_accounts()
        return render_template('index.html')


@app.route('/<token>', methods = ['GET'])
def index_after_confirmation(token):
    user = verify_token(token)
    if user:
        confirm_account(user)
        flash("Account Confirmed!", "info")
    else:
        flash("Link is invalid or expired", "danger")
    return redirect(url_for('index'))


@app.route('/message')
def message():
    flash("Message page is still under konstruction!")
    return redirect(url_for('index'))


@app.route('/user/<username>', methods = ['GET', 'POST'])
def user(username):
    human = Profile.query.filter_by(username=username).first()

    if human is None:
        session.clear()
        flash("Invalid username, this user does not exist")
        return redirect(url_for('index'))

    ls = list_all_friend_stories()

    return render_template('user.html', list_stories=ls)


# if you decide to add reset password to user page
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_route():
    if request.method == 'POST':
        user = Profile.query.filter_by(username = session['username']).first
        password1 = request.form['password1']
        password2 = request.form['password2']
        return reset_password(user, password1, password2)
    else:
        return render_template('reset_password.html', title='Reset Password')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    if request.method == 'POST':
        print("Im almost there")
        user = verify_token(token)
        if user:
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            print(password1)
            return reset_password(user, password1,password2)
        else:
            flash("Link is expired or invalid", "danger")
            return render_template('reset_password.html', title='Reset Password')
    else:
        return render_template('reset_password.html', title='Reset Password')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password_route():
    if request.method == 'POST':
        email = request.form['email']
        return forgot_password(email)
    else:
        return render_template('forgot_password.html', title='Forgot Password')


@app.route('/feed', methods = ['GET', 'POST'])
def feed():
    ls = []
    ls = list_all_friend_stories()
    
    if request.method == 'POST':
        new_story = Story()
        new_story.text = request.form['story_text']
        new_story.username = session['username']
        new_story.user_id = session['id']
        new_story.time = datetime.now().strftime("%d/%m/%Y")
        
        db.session.add(new_story)
        db.session.commit()
        
        if (isinstance(ls,list)):
            ls.append(new_story)
        else:
            ls = [new_story]
            
        return jsonify({'success' : "Story posted!"})
    
    return render_template('feed.html', list_stories=ls)

#This displays a page where you can see all profiles from Folunga that are not your friends
@app.route('/make_new_friends', methods = ['GET', 'POST'])
def make_new_friends():
    if request.method == 'POST':
        return add_friend(request.form['new_friend_id'])

    all_friends = get_id_friends()
    all_friends.append(session['id'])
    ls = list_all_friend_stories()

    return render_template('make_new_friends.html',  users = Profile.query.filter(Profile.id.notin_(all_friends)).all(), list_stories=ls)

@app.route('/friends')
def friends():
    all_friends = get_id_friends()

    ls = list_all_friend_stories()

    return render_template('friends.html',  list_friends = Profile.query.filter(Profile.id.in_(all_friends)).all(), list_stories=ls)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
