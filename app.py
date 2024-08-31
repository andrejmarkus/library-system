from flask import Flask
from flask_login import LoginManager, current_user
from flask_mongoengine import MongoEngine
from configparser import ConfigParser

from admin import admin
from auth import auth
from general import general
from models import User

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth)
app.register_blueprint(general)

db = MongoEngine()
config = ConfigParser()
config.read('config.ini')
app.config['MONGODB_SETTINGS'] = {
    'db': config['MONGO_SETTINGS']['MONGO_DATABASE_NAME'],
    'host': config['MONGO_SETTINGS']['MONGO_DATABASE_URI']
}
app.config['SECRET_KEY'] = config['FLASK_SETTINGS']['SECRET_KEY']

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects.filter(id=user_id).first()

@app.context_processor
def inject_user():
    return dict(user=current_user)

if __name__ == '__main__':
    app.run()
