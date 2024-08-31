from flask import render_template, Blueprint

general = Blueprint('general', __name__, template_folder='templates', static_folder='static')

@general.route('/')
def index():
    return render_template('general/index.html')