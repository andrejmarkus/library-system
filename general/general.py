from flask import render_template, Blueprint, request

from borrowing import borrowing
from models import Book

general = Blueprint('general', __name__, template_folder='templates', static_folder='static')

@general.route('/')
def index():
    books = Book.objects(borrowing__exists=False)
    return render_template('general/index.html', books=books)

@general.get('/search')
def search():
    books = Book.objects().search_text(request.args['value']).order_by('$text_score')
    return render_template('general/index.html', books=books)