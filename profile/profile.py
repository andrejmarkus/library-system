import bcrypt
from flask import Blueprint, request, render_template, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from io import BytesIO

from models import User, Book
from utils import is_file_allowed

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static')

@profile.route('/')
@login_required
def profile_index():
    books = Book.objects(borrowing__user=current_user).order_by("+author", "+title")
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
        return redirect(url_for('profile.profile_settings'))

    user = User.objects(id=current_user.id).first()
    user.profile_picture.replace(file, content_type=file.content_type)
    user.save()

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

@profile.get('/load/<user_id>')
def load_user_image(user_id):
    user = User.objects(id=user_id).first()
    file_data = user.profile_picture.read()
    content_type = user.profile_picture.content_type
    return send_file(BytesIO(file_data), mimetype=content_type, as_attachment=False)

