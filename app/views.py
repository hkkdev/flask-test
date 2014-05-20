# -*- coding: utf-8 -*-
# views.py

from flask.ext.login import LoginManager, login_user, login_required, \
                            current_user, logout_user
from flask import Flask, request, session, g, redirect, url_for, \
                  render_template, flash
from app import app
from werkzeug.security import generate_password_hash, \
                              check_password_hash
from models import *
from forms import LoginForm, SignUpForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginwtf'
login_manager.login_message = u'need to login'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

# some functions
def check_password(password, entered):
    return check_password_hash(password, entered)

def set_password(password):
    return generate_password_hash(password)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def home():
    # list posts
    posts = Posts.query.limit(10)
    return render_template('home.html', posts = posts)

@app.route('/loginwtf', methods=['Get', 'Post'])
def loginwtf():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        login_user(user)
        flash('%s, logged in successfully' % current_user.username)
        return redirect(url_for('home'))
    return render_template('loginwtf.html', form=form)

@app.route('/testing')
@login_required
def testinglogin():
    return "%s, login works" % current_user.username

@app.route("/logoutwtf")
@login_required
def logoutwtf():
    flash("%s, logged out." % g.user.username)
    logout_user()
    return redirect(url_for('loginwtf'))

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

@app.route('/signupwtf', methods = ['GET', 'POST'])
def signupwtf():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, 
                        password=set_password(form.password.data), 
                        email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('signupwtf.html', form=form)

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
            u = g.user
            
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
        if g.user.is_authenticated():
            return render_template('newpost.html')
        if not session.get('user', None):
            return redirect(url_for('home'))
        return render_template('newpost.html')

@app.route('/post/<post_id>', methods = ['GET', 'POST'])
def entry(post_id):
    if request.method == 'POST':
        comment = request.form['comment']
        if not comment:
            flash('Invalid comment')
            return redirect(url_for('entry', post_id=post_id))

        # valid comment adding to Comments
        else:
            u = User.query.filter_by(username=session['user']).first()
            p = Posts.query.filter_by(id=post_id).first()
            c = Comments(comment = comment,
                         post = p,
                         author = u)
            db.session.add(c)
            db.session.commit()
            ent = Posts.query.filter_by(id=post_id).first()
            com = Comments.query.filter_by(post_id=ent.id).all()
            return render_template('single_post.html', 
                                   entry = ent,
                                   comments = com)
            

    # GET
    else:
        ent = Posts.query.filter_by(id=post_id).first()
        if ent:
            com = Comments.query.filter_by(post_id=ent.id).all()
            return render_template('single_post.html', 
                                   entry = ent, 
                                   comments = com)
        else:
            flash('Invalid post')
            return redirect(url_for('home'))




# NOThiNG HERE
