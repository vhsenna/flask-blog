from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    slug = db.Column(db.String(250))
    content = db.Column(db.Text)
    # author = db.Column(db.String(150))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign key to link users
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    about = db.Column(db.Text(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    profile_image = db.Column(db.String, nullable=True)
    password_hash = db.Column(db.String(128))
    # User can have many posts
    posts = db.relationship('Post', backref='poster')

    @property
    def password(self):
        raise AttributeError('Password is not a readable atribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
