from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security import login_user
from flask_security.utils import hash_password, verify_password
from flask_caching import Cache
from loguru import logger
import time
#import logging
#für logging werde ich danach middelware benutzen


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'myapp'})
logger.add("app.log", level="INFO", rotation="1 minute", compression="zip")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SECRET_KEY'] = 'MY_SECRET'
app.config['SECURITY_PASSWORD_SALT'] = 'MY_SECRET_SALT'

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

articles = [
    {"id": 1, "name": "Produkt 1", "price": 19.99},
    {"id": 2, "name": "Produkt 2", "price": 29.99},
    {"id": 3, "name": "Produkt 3", "price": 39.99},
]

def log_message(route):
    logger.info(f"Caching activity on route '{route}'")

def simulate_error():
    # Simuliere einen Fehler und logge ihn
    try:
        log_message("blabla")
        1 / 0  # Dies wird einen ZeroDivisionError auslösen
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
@app.route('/home')
@cache.memoize(timeout=600)
def home():
    time.sleep(5)
    log_message('home')

    simulate_error()
    return render_template('home.html', articles=articles)

@app.route('/signup', methods=['POST', 'GET'])
@cache.memoize(timeout=600)
def register():
    if request.method == 'POST':
        user_datastore.create_user(
            email=request.form.get('email'),
            password=hash_password(request.form.get('password'))
        )
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('index.html')

@app.route('/signin', methods=['POST','GET'])
@cache.memoize(timeout=600)
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Email: {email}, Password: {password}")

        user = user_datastore.get_user(email)

        if user and verify_password(password, user.password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            print("Authentication failed")

    return render_template('signin.html')

@app.route('/profile')
@cache.cached(timeout=600)
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    '''
    with app.app_context():
        db.create_all()

        # Überprüfen Sie, ob der Benutzer bereits existiert
        existing_user = user_datastore.get_user('john@example.com')
        if not existing_user:
            # Beispiel: Füge einen Benutzer zur Datenbank hinzu
            new_user = user_datastore.create_user(email='john@example.com', password='pass123')
            db.session.commit()

            # Beispiel: Füge eine Rolle hinzu und weise sie dem Benutzer zu
            role = user_datastore.create_role(name='admin', description='Administrator')
            user_datastore.add_role_to_user(new_user, role)
            db.session.commit()
        else:
            print('Benutzer existiert bereits.')

        # Beispiel: Rufe alle Benutzer aus der Datenbank ab
        all_users = User.query.all()
        for user in all_users:
            print(f'ID: {user.id}, Email: {user.email}, Roles: {user.roles}')
    '''

    app.run(debug=True)
