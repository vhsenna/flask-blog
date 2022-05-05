from config import Config
from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create a Flask instance
app = Flask(__name__)
app.config.from_object(Config)

# Add database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask_Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add CKEditor
ckeditor = CKEditor(app)

# Static image folder
UPLOAD_FOLDER='app/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import errors, forms, models, routes
