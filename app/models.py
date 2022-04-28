import email
from unicodedata import name
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.name}>'
