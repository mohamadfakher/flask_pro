#app_factory.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_flask_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db = SQLAlchemy(app)
    app.db = db
    return app