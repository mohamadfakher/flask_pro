from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.utils import hash_password


app = Flask(__name__)
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


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_datastore.create_user(
            email=request.form.get('email'),
            password=hash_password(request.form.get('password'))
        )
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('index.html')

@app.route('/profile')
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
