from flask import Flask, request, render_template, redirect
from flask_mongoengine import MongoEngine
from configparser import ConfigParser

from models import Book

app = Flask(__name__)

db = MongoEngine()
config = ConfigParser()
config.read('config.ini')
print(config['MONGO_SETTINGS']['MONGO_DATABASE_URI'])
app.config['MONGODB_SETTINGS'] = {
    'db': config['MONGO_SETTINGS']['MONGO_DATABASE_NAME'],
    'host': config['MONGO_SETTINGS']['MONGO_DATABASE_URI']
}
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    books = Book.objects()
    return render_template('admin/admin.html', books = books)

@app.post('/add-book')
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
    return redirect('/')

if __name__ == '__main__':
    app.run()
