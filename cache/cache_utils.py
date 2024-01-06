#cache_utils.py
from flask_caching import Cache
from utils import log_message
from products.products import Products
from app_factory import create_flask_app

app = create_flask_app()


cache = Cache()

def configure_cache(app):
    cache.init_app(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': 'redis://localhost:6379/0',  # Hier die Redis-Verbindungsdaten eintragen
        'CACHE_DEFAULT_TIMEOUT': 300
    })

def cache_key(route):
    return f"{route}: version1"

def get_data_from_database():
    # Hier könntest du den Code zum Abrufen der Daten aus der Datenbank implementieren
    products = Products.query.all()
    return products
def get_product_by_id(products, product_id):
    for product in products:
        if product.id == product_id:
            return product
    return None
def get_data_with_caching(route):
    cached_data = cache.get(cache_key(route))
    if cached_data is not None:
        log_message(f"Cache hit for route '{route}'")
        return cached_data
    else:
        log_message(f"Cache miss for route '{route}'")
        data = get_data_from_database()
        cache.set(cache_key(route), data)
        return data

def get_product_by_id_with_caching(route, product_id):
    cached_data = cache.get(cache_key(route))
    if cached_data is not None:
        log_message(f"Cache hit for route '{route}'")
        return get_product_by_id(cached_data, product_id)
    else:
        log_message(f"Cache miss for route '{route}'")
        data = get_data_from_database()
        cache.set(cache_key(route), data)
        return get_product_by_id(data, product_id)