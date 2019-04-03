import datetime
import logging
import jwt

from Utilities.CustomExceptions import UserException


class Authentication:
    @staticmethod
    def encode_auth_token(secret_key, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=0, minutes=15, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS512'
            )
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            return Exception('User cannot be logged in. Please, contact with support.')

    @staticmethod
    def decode_auth_token(secret_key, auth_token):
        try:
            payload = jwt.decode(auth_token, secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            msg = 'Signature expired. Please log in again.'
            logging.getLogger('logger').warning(msg)
            raise UserException(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Please log in again.'
            logging.getLogger('logger').warning(msg)
            raise UserException(msg)

