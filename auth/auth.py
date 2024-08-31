import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import User

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.post('/login')
def login_post():
    user = User.objects.filter(username=request.form['username'])

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.post('/signup')
def signup_post():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    user = User.objects(email=email).first()

    if user:
        flash('Email already registered')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password=hashed_password, salt=salt)
    new_user.save()

    return redirect(url_for('auth.login'))