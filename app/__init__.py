from config import Config
from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ckeditor = CKEditor(app)

UPLOAD_FOLDER='static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import errors, forms, models, routes
