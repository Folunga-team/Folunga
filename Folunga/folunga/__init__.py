import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_mail import Mail
# from validate_email import validate_email

app = Flask(__name__, template_folder='templates',  static_url_path='',static_folder="static",)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///folunga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

mail = Mail(app)
# this is for the session
app.secret_key = "folubeautiful"
app.permanent_session_lifetime = timedelta(hours=1)
CORS(app)

from folunga import routes
