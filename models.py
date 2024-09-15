import mongoengine as me
from flask_login import UserMixin


class User(UserMixin, me.Document):
    username = me.StringField(max_length=50, required=True, unique=True)
    email = me.StringField(max_length=50, unique=True)
    password = me.StringField(max_length=256, required=True)
    profile_picture = me.StringField(max_length=100, default='default.jpg')
    role = me.StringField(max_length=50, default='user')


class Borrowing(me.EmbeddedDocument):
    user = me.ReferenceField(User)


class Book(me.Document):
    title = me.StringField(max_length=50, required=True)
    author = me.StringField(max_length=50, required=True)
    publisher = me.StringField(max_length=50, required=True)
    year = me.IntField(required=True)
    description = me.StringField()
    genre = me.StringField(max_length=50, required=True)
    borrowing = me.EmbeddedDocumentField(Borrowing, default=None)
    book_picture = me.StringField(max_length=100)

    meta = { 'indexes': [
        {
            'fields': [ '$title', '$author', '$publisher' ],
            'default_language': 'english',
            'weights': { 'title': 2, 'author': 1, 'publisher': 1 },
        },
    ] }