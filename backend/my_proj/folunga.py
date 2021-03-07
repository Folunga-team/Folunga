from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '8368eb2173ff84a8b30c0d840ed37ec7'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Folunga Home Page')

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit() or (form.username.data == "admin" and form.password.data == "MIPT"):
        flash("You are logged in!")
        return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please chec username and password')

    return render_template('login.html', title='Login', form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Congratlations {form.username.data} has successfully joined Folunga')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)
