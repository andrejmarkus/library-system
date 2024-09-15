from flask import render_template, Blueprint, request, send_from_directory, current_app, redirect, url_for
from flask_login import login_required, current_user

from models import Book, Borrowing, User

general = Blueprint('general', __name__, template_folder='templates', static_folder='static')

@general.route('/')
def index():
    books = Book.objects(borrowing__exists=False).order_by("+author", "+title")
    return render_template('general/index.html', books=books)

@general.get('/search')
def search():
    books = Book.objects(borrowing__exists=False).search_text(request.args['query']).order_by('$text_score')
    return render_template('general/index.html', books=books)

@general.get('/load/<filename>')
def load_book_image(filename):
    return send_from_directory(f'{current_app.config['UPLOAD_FOLDER']}books/', filename)

@general.get('/detail/<book_id>')
def detail_book(book_id):
    book = Book.objects(id=book_id).first()
    users = User.objects(role__ne="admin")
    user_borrowing = book.borrowing.user if book.borrowing else None

    return render_template('general/detail.html', book=book, users=users, user_borrowing=user_borrowing)

@general.post('/return/<user_id>/<book_id>')
@login_required
def borrow_return(user_id, book_id):
    if current_user.role != 'admin':
        return redirect(url_for('general.index'))

    user = User.objects(id=user_id).first()
    Book.objects(id=book_id).update(unset__borrowing=True)

    return redirect(url_for('admin.user_profile', user_id=user.id))