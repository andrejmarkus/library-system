from flask import render_template, Blueprint
from flask_login import current_user

general = Blueprint('general', __name__, template_folder='templates', static_folder='static')

@general.route('/')
def index():
    return render_template('general/index.html', user=current_user)