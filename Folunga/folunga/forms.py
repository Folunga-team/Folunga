from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired("Please enter a username"), Length(min=2, max=20)])
    email = EmailField('Email',
                            validators=[DataRequired("Please enter an email address"), Email("Invalid email")])
    password = PasswordField('Password', validators=[DataRequired("Password cannot be empty")])
    confirm_password = PasswordField('Confirm_password', validators=[EqualTo('password', " Passwords do not match.")])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired("Please enter a username"), Length(min=2, max=20)])
    # email = EmailField('Email',
    #                         validators=[DataRequired("Please enter an email address"), Email("Invalid email")])
    password = PasswordField('Password', validators=[DataRequired("Password cannot be empty")])
    # remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
