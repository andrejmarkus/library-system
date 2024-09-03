import os

from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import User, Book
from utils import is_file_allowed, file_extension

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static')

@profile.route('/', methods=['GET', 'PUT'])
@login_required
def profile_index():
    books = Book.objects(borrowing__user_id=current_user.id)
    return render_template('profile/profile.html', books=books)

@profile.route('/edit-profile')
@login_required
def edit_profile():
    return render_template('profile/edit-profile.html')

@profile.post('/upload')
@login_required
def upload():
    file = request.files['file']
    if not is_file_allowed(file.filename):
        flash('File not allowed', 'danger')
        return redirect(url_for('profile.edit_profile'))
    filename = secure_filename(f'{current_user.id}{file_extension(file.filename)}')
    path = os.path.join(f'{current_app.config['UPLOAD_FOLDER']}users/{current_user.id}/', filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)

    User.objects(id=current_user.id).update(profile_picture=filename)

    return redirect(url_for('profile.edit_profile'))


@profile.get('/load/<user_id>/<filename>')
def load_user_image(user_id, filename):
    return send_from_directory(f'{current_app.config['UPLOAD_FOLDER']}users/{user_id}/', filename)

