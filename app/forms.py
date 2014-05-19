from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from models import *

from werkzeug.security import generate_password_hash, \
                              check_password_hash

def check_password(password, entered):
    return check_password_hash(password, entered)

def set_password(password):
    return generate_password_hash(password)

class Password_Check(object):
    def __init__(self, message=None):
        if not message:
            message = u'Invalid pw/username'
        self.message = message

    def __call__(self, form, field):
        l = len(field.data)
        if l < 4 or  l > 25:
            raise ValidationError(self.message)
        user = form.username.data
        user_in_db = User.query.filter_by(username=user).first()
        if not user_in_db or  \
           not check_password(user_in_db.password, field.data):
            raise ValidationError(self.message)

class LoginForm(Form):
    username = TextField('username', validators=[
        DataRequired(message="Username required"),
        Length(min=4, max=25, message='Please check username')
        ])
    password = PasswordField('password', validators=[
        DataRequired(message="Password required"),
        Password_Check()
        ])

        













    
