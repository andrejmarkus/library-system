import os

from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory
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
    file.save(os.path.join('static/', filename))

    User.objects(id=current_user.id).update(profile_picture=filename)

    return redirect(url_for('profile.edit_profile'))


@profile.get('/load/<filename>')
@login_required
def load(filename):
    return send_from_directory('static/', filename)

