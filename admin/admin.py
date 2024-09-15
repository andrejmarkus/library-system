import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import Book, User, Borrowing
from utils import is_file_allowed, file_extension

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    users = User.objects(id__ne=current_user.id).order_by('+role', '+username')
    return render_template('admin/users.html', users=users)

@admin.route('/books')
@login_required
def books():
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    books = Book.objects().order_by("+author", "+title")
    return render_template('admin/books.html', books=books)

@admin.route('/profile/<user_id>')
@login_required
def user_profile(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    user = User.objects(id=user_id).first()
    books = Book.objects(borrowing__user=user).order_by("+author", "+title")

    return render_template('admin/user-profile.html', display_user=user, books=books)

@admin.delete('/users/delete/<user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    user = User.objects(id=user_id).first()

    if user.profile_picture != 'default.jpg':
        os.remove(os.path.join(f'{current_app.config['UPLOAD_FOLDER']}users/', user.profile_picture))

    Book.objects(borrowing__user=user).update(unset__borrowing=True)
    user.delete()

    return Response(status=200)

@admin.post('/users/role/<user_id>')
@login_required
def change_role(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    role = request.json['role']

    User.objects(id=user_id).update(role=role)
    return redirect(url_for('admin.users'))

@admin.post('/books/add')
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
    path = os.path.join(f'{current_app.config['UPLOAD_FOLDER']}books/', filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)

    book.update(book_picture=filename)

    return redirect(url_for('admin.books'))

@admin.delete('/books/delete/<book_id>')
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    book = Book.objects(id=book_id).first()
    os.remove(os.path.join(f'{current_app.config['UPLOAD_FOLDER']}books/', book.book_picture))

    book.delete()
    return Response(status=200)

@admin.post('/books/borrow/<book_id>')
@login_required
def borrow(book_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    user_id = request.form['user_id']

    user = User.objects(id=user_id).first()
    borrowing = Borrowing(user=user)
    Book.objects(id=book_id).update(borrowing=borrowing)

    return redirect(url_for('admin.user_profile', user_id=user.id))