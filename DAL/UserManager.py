import hashlib
import logging

from ORM import db
from ORM.User import User

from Utilities.CustomExceptions import UserException, DatabaseException


class UserManager:
    @staticmethod
    def create_user(login, password):
        try:
            if not db.session.query(User).filter(User.login == login).first():
                new_user = User(login=login, password=password)
                db.session.add(new_user)
                db.session.commit()
                return new_user
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

        msg = 'User with this email already exists'
        logging.getLogger('logger').warning(msg)
        raise UserException(msg)

    @staticmethod
    def read_user(login, password):
        try:
            user = db.session.query(User).filter(User.login == login).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
        if user:
            hash_password = hashlib.sha3_512(password.encode('utf-8') + user.salt.encode('utf-8')).hexdigest()
            if user.hashed_password == hash_password:
                logging.getLogger('logger').info('User ' + user.login + ' was found.')
                return user
            else:
                logging.getLogger('logger').warning('Wrong password for ' + user.login + ' user.')
                raise UserException()
        else:
            logging.getLogger('logger').warning('Cannot find user.')
            raise UserException()

    @staticmethod
    def update_user(user):
        try:
            hash_password = hashlib.sha3_512(user.hashed_password.encode('utf-8') +
                                             user.salt.encode('utf-8')).hexdigest()
            db.session.query(User).filter(User.id == user.id).\
                update({'login': user.login, 'hashed_password': hash_password})
            db.session.commit()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def delete_user(user_id):
        try:
            db.session.query(User).filter(User.id == user_id).delete()
            db.session.commit()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get_user(user_id):
        try:
            return db.session.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()


