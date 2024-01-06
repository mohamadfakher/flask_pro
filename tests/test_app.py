#test_app.py

import unittest
from app_factory import create_flask_app
from auth.auth import *


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app = create_flask_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECURITY_PASSWORD_SALT'] = 'salt'

        self.app = app.test_client()
        self.app_context = app.test_request_context()
        self.app_context.push()
        with app.app_context():
            db.init_app(app)
            db.create_all()


    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_signup_successful(self):
        with self.app.app_context():
            response = self.app.post('/auth/signup', data=dict(
                email='test@gmail.com',
                password='test@gmail.com',
                confirm_password='test@gmail.com'
            ), follow_redirects=True)

        user = User.query.filter_by(email='test@gmail.com').first()
        self.assertTrue(user)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created! You can now log in.', response.data)

if __name__ == '__main__':
    unittest.main()