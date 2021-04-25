from flask import render_template, url_for, flash, redirect, request, session, jsonify
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
            new_profile.username = request.form['username']
            new_profile.first_name = request.form['first_name']
            new_profile.last_name = request.form['last_name']
            new_profile.email = request.form['email']
            new_profile.date_birth = request.form['date_birth']

            if request.form['password'] != request.form['password2']:
                return jsonify({'error' : "Passwords do not match"})
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            new_profile.password = hashed_password
            return register(new_profile)

        elif request.form.get('form') == 'recovery_password':
            print("what now!")
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

    lst_friends = friend_list_generator(human.id)

    return render_template('user.html', human = human, num_friends = len(lst_friends), lst_prt_stories = printable_stories_person(human))


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
            password1 = request.form['password1']
            password2 = request.form['password2']
            print(password2)
            return reset_password(user, password1, password2)
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


@app.route('/user/<username>/friends')
def friends(username):
    # DO something, hellllllpppppppppppppppppppppppppppppppp
    who_all_are_this_guys_friends= Profile.query.all()
    return inject_friend_list('all', who_all_are_this_guys_friends)


@app.route('/all_profiles')
def all_profiles():
    return inject_friend_list('all', Profile.query.all())


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
