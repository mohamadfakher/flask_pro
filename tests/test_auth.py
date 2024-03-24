#test_auth.py
import sys
import os

# Füge das Wurzelverzeichnis zum sys.path hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from flask_testing import TestCase
from flask import url_for
from config import db, create_app
from auth.auth import User

class TestAuthBlueprint(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        response = self.client.get('/auth/signup')
        self.assert200(response)

    def test_lgoin(self):
        response = self.client.get('/auth/login')
        self.assert200(response)

    def test_profile_requires_login(self):
        response = self.client.get('/auth/profile')
        expected_location = url_for('security.login', next='/auth/profile')
        self.assertRedirects(response, expected_location)

    def test_profile_requires_logout(self):
        response = self.client.get('/auth/logout')
        expected_location = url_for('security.login', next='/auth/logout')
        self.assertRedirects(response, expected_location)

    def test_signup_form_submission(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'test@gmail.com',
            'confirm_password': 'test@gmail.com'
        }
        response = self.client.post('/auth/signup', data=data)
        self.assertRedirects(response, '/auth/login')
        login_page_response = self.client.get('/auth/login')
        self.assertIn(b'Your account has been created!', login_page_response.data)

    def test_login_form_submission(self):
        user = User(email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'remember': False
        }
        response = self.client.post('/auth/login', data=data, follow_redirects=True)
        self.assert200(response)
        profile_page_response = self.client.get('/auth/profile')
        self.assertIn(b'profile', profile_page_response.data)

    def test_form_validation_errors(self):
        #signup with invalid data
        invalid_data = {
            'email': 'invalid_email',
            'password': 'short',
            'confirm_password': 'password_mismatch'
        }
        response = self.client.post('/auth/signup', data=invalid_data, follow_redirects=True)
        self.assertIn(b'Invalid email address.', response.data)

        invalid_data = {
            'email': 'invalid_email',
            'password': 'short',
            'remember': False
        }
        response = self.client.post('/auth/login', data=invalid_data, follow_redirects=True)
        self.assertIn(b'Invalid email address.', response.data)


if __name__ == '__main__':
    unittest.main()
