# auth/auth.py
from utils import log_message
from loguru import logger
from config import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, login_user, login_required
from flask_security import logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='user_roles')
    remember_me = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(255), default='profile_image.png')


# This table connects users with roles
user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                      )

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(),
                        EqualTo('password', message='Password must match')])
    submit = SubmitField('Signup')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Register a new user.
    """
    log_message('signup')
    if current_user.is_authenticated:
        return redirect(url_for("auth_blueprint.profile"))

    form = SignupForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('Email is already in use.')
            return redirect(url_for('auth_blueprint.signup'))

        hashed_password = generate_password_hash(password, method='sha256')
        user_datastore.create_user(
            email=email,
            password=hashed_password
        )
        db.session.commit()

        #flash('Your account has been created!', 'success')
        return redirect(url_for('auth_blueprint.login'))
    return render_template('auth/signup.html', form=form)


@auth_bp.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    log_message('signin')
    if current_user.is_authenticated:
        return redirect(url_for("auth_blueprint.profile"))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            user.remember_me = form.remember.data
            db.session.commit()
            return redirect(url_for('auth_blueprint.profile'))

        flash('Invalid email or password. Please try again!!', 'error')
        logger.info("Authentication failed")

    return render_template('auth/login.html', form=form)

@auth_bp.route('profile')
@login_required
def profile():
    log_message("profile")

    return render_template('auth/profile.html')

@auth_bp.route('logout')
@login_required
def logout():
    log_message("logout")
    logout_user()
    return redirect(url_for('auth_blueprint.login'))