#proucts.py

from config import db
from flask import Blueprint

products_bp = Blueprint('products_bp', __name__, template_folder='templates', static_folder='static')

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    price = db.Column(db.Float)
    image_path = db.Column(db.String(255))



