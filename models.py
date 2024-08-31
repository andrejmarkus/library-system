import mongoengine as me


class User(me.Document):
    username = me.StringField(max_length=50, required=True, unique=True)
    email = me.StringField(max_length=50, unique=True)
    salt = me.StringField(required=True)
    password = me.StringField(max_length=256, required=True)
    role = me.StringField(max_length=50, default='user')


class Book(me.Document):
    title = me.StringField(max_length=50, required=True)
    author = me.StringField(max_length=50, required=True)
    publisher = me.StringField(max_length=50, required=True)
    year = me.IntField(required=True)
    description = me.StringField()
    genre = me.StringField(max_length=50, required=True)


class Borrowing(me.Document):
    user_id = me.ReferenceField(User)
    book_id = me.ReferenceField(Book)
    from_date = me.DateTimeField()
    to_date = me.DateTimeField()