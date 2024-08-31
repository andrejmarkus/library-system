from cgitb import reset

import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import User

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.post('/login')
def login_post():
    user = User.objects.filter(username=request.form['username']).first()

    if not user:
        flash("User isn't registered")
        return redirect(url_for('auth.login'))

    salt = user.salt
    hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
    result = bcrypt.checkpw(user.password, hash)

    if result:
        return redirect(url_for('/'))

    flash("Incorrect username or password")
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.post('/signup')
def signup_post():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('auth.signup'))

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    user = User.objects(email=email).first()

    if user:
        flash('Email already registered')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password=hashed_password, salt=salt)
    new_user.save()

    return redirect(url_for('auth.login'))