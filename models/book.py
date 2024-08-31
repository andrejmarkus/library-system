from datetime import datetime

import mongoengine as me

from models.user import User


class Book(me.Document):
    title = me.StringField(max_length=50, required=True)
    author = me.StringField(max_length=50, required=True)
    publisher = me.StringField(max_length=50, required=True)
    year = me.IntField(required=True)
    description = me.StringField()
    genre = me.StringField(max_length=50, required=True)

class Borrowing(me.EmbeddedDocument):
    user_id = me.ReferenceField(User)
    from_date = me.DateTimeField(default=datetime.now())
    to_date = me.DateTimeField()