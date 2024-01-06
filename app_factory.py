#app_factory.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_flask_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db = SQLAlchemy(app)  # Erstelle die SQLAlchemy-Erweiterung mit der Flask-Anwendung
    app.db = db  # Füge die db-Erweiterung zur Flask-Anwendung hinzu (optional)
    return app