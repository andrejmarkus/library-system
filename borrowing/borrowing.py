from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models import Book, Borrowing

borrowing = Blueprint('borrowing', __name__, template_folder='templates', static_folder='static')

@borrowing.route('/<book_id>')
@login_required
def borrowing_index(book_id):
    book = Book.objects(id=book_id).first()
    return render_template('borrowing/index.html', book=book)

@borrowing.post('/<book_id>')
@login_required
def borrow(book_id):
    from_date = request.form['from_date']
    to_date = request.form['to_date']

    borrowing = Borrowing(user_id=current_user.id, from_date=from_date, to_date=to_date)
    Book.objects(id=book_id).update(borrowing=borrowing)

    return redirect(url_for('profile.profile_index'))

@borrowing.post('/return/<username>/<book_id>')
@login_required
def borrow_return(username, book_id):
    if current_user.role != 'admin':
        return redirect(url_for('profile.profile_index'))

    Book.objects(id=book_id).update(unset__borrowing=True)

    return redirect(url_for('admin.user_profile', username=username))