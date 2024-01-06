#app.py

from auth.auth import auth_bp
from auth.middleware.auth_middleware import AuthMiddleware
from auth.middleware.request_logger import RequestLoggerMiddleware
from general.general import general_bp
from products.products import Products, products_bp
from products.product_detail import view_bp
from logger.request_logger import AppLogger
from config import db, create_app
from cache.cache_utils import configure_cache

app = create_app()
configure_cache(app)

# Hier nicht benötigt, da bereits in `create_app` aufgerufen
# with app.app_context():
#     db.create_all()

with app.app_context():
    # Hier erstellst du alle Tabellen
    #db.create_all()

    # Hier fügst du Beispieldaten hinzu
    sample_product = Products(name='Sample Product', description='This is a sample product', price=19.99, image_path='product1.png')
    db.session.add(sample_product)
    db.session.commit()

# AuthMiddleware
protected_endpoints = ['profile', 'signin', 'signup']
app.wsgi_app = RequestLoggerMiddleware(app.wsgi_app)
app.wsgi_app = AuthMiddleware(app.wsgi_app, protected_endpoints)

# Konfiguriere den App-Logger
app_logger = AppLogger()
app_logger.get_logger().info("This log message uses the configured logger.")

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth', name='auth_blueprint')
app.register_blueprint(general_bp, url_prefix='/general', name='general_blueprint')
app.register_blueprint(products_bp, url_prefix='/products', name='products_blueprint')
app.register_blueprint(view_bp, url_prefix='/product_detail', name='view_blueprint')

if __name__ == '__main__':
    app.run(debug=True)
