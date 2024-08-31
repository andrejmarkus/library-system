from flask import render_template, Blueprint, request

from models import Book

general = Blueprint('general', __name__, template_folder='templates', static_folder='static')

@general.route('/')
def index():
    books = Book.objects()
    return render_template('general/index.html', books=books)

@general.get('/find')
def find():
    books = Book.objects().search_text(request.args['search']).order_by('$text_score')
    return render_template('general/index.html', books=books)