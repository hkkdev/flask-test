# views.py

from flask import Flask, request, session, g, redirect, url_for, \
                  render_template, flash
from app import app
from werkzeug.security import generate_password_hash, \
                              check_password_hash
from models import *

# some functions
def check_password(password, entered):
    return check_password_hash(password, entered)

def set_password(password):
    return generate_password_hash(password)

@app.route('/')
def home():
    # list posts
    posts = Posts.query.limit(10)
    return render_template('home.html', posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    have_error = False
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        u = User.query.filter_by(username=user).first()
        
        if not find_user(user):
            have_error = True
        elif not check_password(u.password, pw):
            have_error = True
        else:
            session['user'] = user
            session['logged_in'] = True
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

def find_user(user):
    u = User.query.filter_by(username=user).first()
    if u:
        return True
    else:
        return False

def find_email(email):
    if User.query.filter_by(email=email).first():
        return True
    else:
        return False

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
        elif find_user(user):
            params['error_username'] = 'Username exists'
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
        elif find_email(email):
            params['error_email'] = 'Email already in use'
            have_error = True

        if have_error:
            return render_template('signup.html', **params)
        else:
            new_user = User(username=user, 
                            password=set_password(pw), 
                            email=email)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user
            session['logged_in'] = True
            return redirect(url_for('home'))

    # method GET
    return render_template('signup.html')

@app.route('/newpost', methods = ['GET', 'POST'])
def newpost():
    # method POST
    if request.method == 'POST':
            #return redirect(url_for('home'))
        params = {}
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            params['error'] = 'Need both title and content'
            return render_template('newpost.html', **params)
        else:
            u = User.query.filter_by(username=session['user']).first()
            new_entry = Posts(title = title,
                              content = content,
                              author = u
                              )
            db.session.add(new_entry)
            db.session.commit()
            post_id = new_entry.id
            return redirect('/post/%d' % post_id)
    
    # method GET
    else:
        if not session.get('user', None):
            return redirect(url_for('home'))
        return render_template('newpost.html')

@app.route('/post/<post_id>')
def entry(post_id):
    ent = Posts.query.filter_by(id=post_id).first()
    com = Comments.query.filter_by(post_id=ent.id).all()
    if ent:
        return render_template('single_post.html', entry = ent, com = com)
    else:
        return redirect(url_for('home'))




# NOThiNG HERE
