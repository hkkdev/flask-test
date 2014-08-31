# __init__.py

from flask import Flask

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='something',
))

from app import views
