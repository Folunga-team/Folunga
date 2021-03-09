from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), nullable=False)
	last_name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
	password = db.Column(db.String(80), nullable=False)
	likes_count = db.Column(db.Integer, default=0)
	
	def __repr__(self, ):
		return '<User %r>' % self.id
        
@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		pfirst_name = request.form['first_name']
		profile = Profile(first_name = pfirst_name)
		
		profile.last_name= request.form['last_name']
		profile.email = request.form['email']
		pdate_of_birth = request.form['date_of_birth']

		try:
			db.session.add(profile)
			db.session.commit()
			
			return redirect('/')
		except:
			return 'There was an issue adding your task'
            
	else:	
		database = Profile.query.order_by(Profile.email).all()
		#return redirect('/')
		return render_template('index.html', database_profile_range = database)
			
			
if __name__ == "__main__":
    app.run(debug=True)
