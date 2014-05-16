# bullpen

import os
import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, \
                  render_template, flash
from app.models import db, User

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='something',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
))

# db



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    have_error = False
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        find_user = User.query.filter_by(username=user).first()

        if not find_user:
            have_error = True
        elif pw != find_user.password:
            have_error = True
        else:
            session['user'] = user
            session['logged_in'] = True
            flash('logged in as %s' % session['user'])
            return redirect(url_for('home'))
    if have_error:
        error = 'Wrong username or password'
        return render_template('login.html', error=error, username=user)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('logged_in', None)
    flash('Your are logged out')
    return redirect(url_for('home'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        have_error = False
        params = {}
        user = request.form['username']
        pw = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        params['username'] = user
        params['email'] = email

        if not user:
            params['error_username'] = 'Invalid username'
            have_error = True
        if not pw:
            params['error_password'] = 'Invalid password'
            have_error = True
        if not verify:
            params['error_verify'] = 'Invalid password'
            have_error = True
        if pw != verify:
            params['error_verify'] = 'Password does not match'
            have_error = True
        if not email:
            params['error_email'] = 'Invalid email'
            have_error = True
        if have_error:
            return render_template('signup.html', **params)
        else:
            new_user = User(username=user, password=pw, email=email)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user
            session['logged_in'] = True
            return redirect(url_for('home'))

    # method GET
    return render_template('signup.html')
        

if __name__ == '__main__':
    app.run()
