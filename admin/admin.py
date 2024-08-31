from flask import Blueprint, render_template, request, redirect, url_for

from models import Book

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
def admin_index():
    books = Book.objects()
    return render_template('admin/admin.html', books=books)

@admin.post('/add-book')
def add_book():
    book = Book(
        title=request.form['title'],
        author=request.form['author'],
        publisher=request.form['publisher'],
        year=request.form['year'],
        genre=request.form['genre'],
        description=request.form['description']
    )
    book.save()
    return redirect(url_for('admin'))