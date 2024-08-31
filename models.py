import mongoengine as me


class User(me.Document):
    username = me.StringField(max_length=50, required=True, unique=True)
    email = me.StringField(max_length=50, unique=True)
    salt = me.StringField(required=True)
    password = me.StringField(max_length=50, required=True)
    role = me.StringField(max_length=50, default='user')


class Book(me.Document):
    title = me.StringField(max_length=50, required=True)
    author = me.StringField(max_length=50, required=True)
    publisher = me.StringField(max_length=50, required=True)
    year = me.IntField(required=True)
    description = me.StringField()
    genre = me.StringField(max_length=50, required=True)


class Borrowing(me.EmbeddedDocument):
    user_id = me.ReferenceField(User)
    from_date = me.DateTimeField()
    to_date = me.DateTimeField()