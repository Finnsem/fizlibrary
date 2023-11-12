from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Add any additional fields/methods you may need

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    version = db.Column(db.String(50), nullable=False)
    shelf = db.Column(db.String(50), nullable=False)

    # Add any additional fields/methods you may need

class SearchForm(FlaskForm):
    query = StringField('search', validators=[DataRequired()])
    submit = SubmitField('search')

"""
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' https://trustedcssdomain.com;"
    return resp

    
    The Content-Security-Policy header you've set with default-src 'self';
      restricts all content to only be loaded from the same origin as the site. 
      This includes CSS, JavaScript, fonts, iframes, and images. If you have any external
        resources that your HTML pages rely on (like CSS from a CDN, fonts from Google Fonts, 
        or scripts from external sources), they would be blocked by this policy.
"""
