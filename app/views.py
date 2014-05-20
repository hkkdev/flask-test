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
login_manager.login_view = 'login'
login_manager.login_message = u'need to login'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

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

@app.route('/login', methods=['Get', 'Post'])
def login():
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

@app.route("/logout")
@login_required
def logout():
    flash("%s, logged out." % g.user.username)
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
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
        if not g.user.is_authenticated():
            return redirect(url_for('home'))
        return render_template('newpost.html')

@app.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def entry(post_id):
    if request.method == 'POST':
        comment = request.form['comment']
        if not comment:
            flash('Invalid comment')
            return redirect(url_for('entry', post_id=post_id))

        # valid comment adding to Comments
        else:
            u = g.user
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
    # Show post and comments
    else:
        ent = Posts.query.filter_by(id=post_id).first()
        if ent:
            com = Comments.query.filter_by(post_id=ent.id).all()
            return render_template('single_post.html', 
                                   entry = ent, 
                                   comments = com)
        else:
            flash('Post does not exist')
            return redirect(url_for('home'))




# NOThiNG HERE
