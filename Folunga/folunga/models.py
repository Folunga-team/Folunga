from folunga import db
from datetime import datetime

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    date_birth = db.Column(db.String(20), nullable=False)
    profile_pic = db.Column(db.String(50), nullable=False, default='default.jpg')

    user_confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    stories = db.relationship('Story', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"



class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    text = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"Story('{self.text}', '{self.date_posted}'"

class friendship(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	user_first_id = db.Column(db.String(20), nullable=False)
	user_second_id = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f"friendship('{self.user_first_id}', '{self.user_second_id}')"
