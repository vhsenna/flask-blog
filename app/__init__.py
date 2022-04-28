from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

from app import errors, forms, routes
