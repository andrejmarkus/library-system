import bcrypt
from flask import Flask
from flask_mongoengine import MongoEngine
from configparser import ConfigParser

from admin import admin
from auth import auth
from general import general

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth)
app.register_blueprint(general)

db = MongoEngine()
config = ConfigParser()
config.read('config.ini')
print(config['MONGO_SETTINGS']['MONGO_DATABASE_URI'])
app.config['MONGODB_SETTINGS'] = {
    'db': config['MONGO_SETTINGS']['MONGO_DATABASE_NAME'],
    'host': config['MONGO_SETTINGS']['MONGO_DATABASE_URI']
}
db.init_app(app)

if __name__ == '__main__':
    app.run()
