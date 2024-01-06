#prouct_detail.py

from utils import *
from flask import Blueprint, render_template
from cache.cache_utils import get_product_by_id_with_caching

view_bp = Blueprint('view_bp', __name__, template_folder='templates', static_folder='static')

@view_bp.route('/view/<int:product_id>')
def product_detail(product_id):
    log_message('/view/<int:product_id>')

    product = get_product_by_id_with_caching('view', product_id)

    return render_template('products/view.html', product=product)