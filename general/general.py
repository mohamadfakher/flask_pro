from utils import *
from flask import Blueprint, render_template
from cache.cache_utils import get_data_with_caching
from flasgger import swag_from


general_bp = Blueprint('general_blueprint', __name__, template_folder='templates')

@general_bp.route('/home')
def home():
    log_message('home')

    products = get_data_with_caching('home')
    return render_template('general/home.html', products=products)
