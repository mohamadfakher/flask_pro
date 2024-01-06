from flask import redirect, url_for
from flask_security import current_user

class AuthMiddleware:
    def __init__(self, app, protected_endpoints):
        self.app = app
        self.protected_endpoints = set(protected_endpoints)

    def is_protected_endpoint(self, endpoint):
        return endpoint in self.protected_endpoints

    def redirect_to_login(self):
        return redirect(url_for('signin'))

    def __call__(self, environ, start_response):
        if self.is_protected_endpoint(environ.get('ENDPOINT')):
            if not current_user.is_authenticated:
                return self.redirect_to_login()

        return self.app(environ, start_response)