import os

import bcrypt
from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import User, Book
from utils import is_file_allowed, file_extension

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static')

@profile.route('/')
@login_required
def profile_index():
    books = Book.objects(borrowing__user=current_user)
    return render_template('profile/profile.html', books=books)

@profile.route('/settings')
@login_required
def profile_settings():
    return render_template('profile/edit-profile.html')

@profile.post('/upload')
@login_required
def upload():
    file = request.files['file']
    if not is_file_allowed(file.filename):
        flash('File not allowed', 'danger')
        return redirect(url_for('profile.edit_profile'))
    filename = secure_filename(f'{current_user.id}{file_extension(file.filename)}')
    path = os.path.join(f'{current_app.config['UPLOAD_FOLDER']}users/', filename)

    user = User.objects(id=current_user.id).first()

    if user.profile_picture != 'default.jpg':
        os.remove(os.path.join(f'{current_app.config['UPLOAD_FOLDER']}users/', user.profile_picture))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)
    user.update(profile_picture=filename)

    return redirect(url_for('profile.profile_settings'))

@profile.post('/update-username')
@login_required
def update_username():
    username = request.form['username']
    User.objects(id=current_user.id).update(username=username)

    return redirect(url_for('profile.profile_settings'))

@profile.post('/update-password')
@login_required
def update_password():
    new_password = request.form['new_password']
    old_password = request.form['old_password']

    result = bcrypt.checkpw(old_password.encode('utf-8'), current_user.password.encode('utf-8'))

    if result:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

        User.objects(id=current_user.id).update(password=hashed_password)
        return redirect(url_for('profile.profile-settings'))

    flash("Invalid password")
    return redirect(url_for('profile.profile_settings'))

@profile.get('/load/<filename>')
def load_user_image(filename):
    return send_from_directory(f'{current_app.config['UPLOAD_FOLDER']}users/', filename)

