from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
# from validate_email import validate_email

app = Flask(__name__, template_folder='templates',  static_url_path='',static_folder="static",)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///folunga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# this is for the session
app.secret_key = "folubeautiful"
app.permanent_session_lifetime = timedelta(hours=1)
CORS(app)

from folunga import routes
