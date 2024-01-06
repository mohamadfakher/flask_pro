from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from app_factory import create_flask_app

db = SQLAlchemy()

def configure_security(app, user_datastore):
    Security(app, user_datastore)

def create_app():
    app = create_flask_app()
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SECURITY_PASSWORD_SALT'] = 'salt'
    #for the warning of SQLALCHEMY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from auth.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.init_app(app)
        from auth.auth import User, Role
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        configure_security(app, user_datastore)
        db.create_all()

    return app
