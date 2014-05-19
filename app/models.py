# models.py

from app import app, db
from flask.ext.sqlalchemy import SQLAlchemy

USER = 0
ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(256))
    role = db.Column(db.SmallInteger, default = USER)
    posts = db.relationship('Posts', 
                             backref = 'author', 
                             lazy = 'dynamic')
    comments = db.relationship('Comments',
                                backref = 'author',
                                lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text(100), index = True)
    content = db.Column(db.Text(250), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comments',
                                backref = 'post',
                                lazy = 'dynamic')

    def __repr__(self):
        return '<Post %r>' % (self.content)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text(100), index = True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.comment)
