from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from borrowing import borrowing
from models import Book, User

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

    Book(
        title=request.form['title'],
        author=request.form['author'],
        publisher=request.form['publisher'],
        year=request.form['year'],
        genre=request.form['genre'],
        description=request.form['description']
    ).save()

    return redirect(url_for('admin.admin_index'))

@admin.delete('/delete-book/<book_id>')
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    book = Book.objects(id=book_id)
    book.delete()
    return redirect(url_for('admin.admin_index'))