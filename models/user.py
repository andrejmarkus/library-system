import mongoengine as me

class User(me.Document):
    name = me.StringField(max_length=50, required=True)
    email = me.StringField(max_length=50)
    password = me.StringField(max_length=50, required=True)
    role = me.StringField(max_length=50, default='user')
