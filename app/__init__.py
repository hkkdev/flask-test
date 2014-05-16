# __init__.py

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='something',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
))

db = SQLAlchemy(app)

from app import views, models
