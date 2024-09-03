import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import Book, User
from utils import is_file_allowed, file_extension

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
@login_required
def admin_index():
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    books = Book.objects()
    return render_template('admin/admin.html', books=books)

@admin.route('/user/<username>')
@login_required
def user_profile(username):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    user = User.objects(username=username).first()
    books = Book.objects(borrowing__user_id=user.id)

    return render_template('admin/user-profile.html', display_user=user, books=books)

@admin.post('/add-book')
@login_required
def add_book():
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    file = request.files['file']

    if file is None:
        flash('Please upload a file', 'error')
        return redirect(url_for('admin.admin_index'))

    if not is_file_allowed(file.filename):
        flash('File not allowed', 'danger')
        return redirect(url_for('admin.admin_index'))

    book = Book(
        title=request.form['title'],
        author=request.form['author'],
        publisher=request.form['publisher'],
        year=request.form['year'],
        genre=request.form['genre'],
        description=request.form['description']
    ).save()

    filename = secure_filename(f'{book.id}{file_extension(file.filename)}')
    path = os.path.join(f'{current_app.config['UPLOAD_FOLDER']}books/{book.id}/', filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)

    book.update(book_picture=filename)

    return redirect(url_for('admin.admin_index'))

@admin.delete('/delete-book/<book_id>')
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    book = Book.objects(id=book_id)
    book.delete()

    return redirect(url_for('admin.admin_index'))
