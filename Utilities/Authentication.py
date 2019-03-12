from flask import request
import hashlib


class Authentication:
    @staticmethod
    def generate_auth_token(username, password):
        token = hashlib.sha512(username.encode('utf-8')
                                 + password.encode('utf-8')
                                 + request.headers.get('User-Agent').encode('utf-8')).hexdigest()
        return token

    @staticmethod
    def verify_auth_token(token, new_token):
        if token:
            if token == new_token:
                return True
            return False
