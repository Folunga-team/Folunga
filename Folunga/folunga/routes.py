from flask import render_template, url_for, flash, redirect, request, session, jsonify
from folunga import app
from folunga.forms import LoginForm, RegistrationForm
from folunga.functions import *

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

@app.route('/message')
def message():
    return display_error("Message page is still under konstruction!")


@app.route('/user/<username>', methods = ['GET', 'POST'])
def user(username):
    human = Profile.query.filter_by(username=username).first()

    if human is None:
        return display_error("Invalid username, this user does not exist")

    lst_friends = friend_list_generator(human.id)

    return render_template('user.html', human = human, num_friends = len(lst_friends), lst_prt_stories = printable_stories_person(human))


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
