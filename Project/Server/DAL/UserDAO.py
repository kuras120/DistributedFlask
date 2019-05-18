import os
import shutil
import hashlib
import logging

from Project.Server.ORM import db
from Project.Server.ORM.User import User
from Project.Server.ORM.History import History, TypeH

from Project.Server.Utilities.CustomExceptions import UserException, DatabaseException


class UserDAO:
    @staticmethod
    def create(login, password):
        try:
            if not db.session.query(User).filter(User.login == login).first():
                new_user = User(login=login, password=password)
                h_log = History(type_h=TypeH.Info, description='Account created')
                new_user.history.append(h_log)
                db.session.add(new_user)
                db.session.commit()
                path = 'Project/Server/DATA/' + new_user.home_catalog
                if not os.path.isdir(path):
                    os.makedirs(path)
                return new_user
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

        msg = 'User with ' + login + ' already exists.'
        logging.getLogger('logger').warning(msg)
        raise UserException(msg)

    @staticmethod
    def read(login, password):
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
                raise UserException('Wrong username or password.')
        else:
            logging.getLogger('logger').warning('Cannot find user ' + login + '.')
            raise UserException('Wrong username or password.')

    @staticmethod
    def update(user, info=None):
        if user:
            try:
                if info:
                    h_log = History(type_h=TypeH.Info, description=info)
                    user.history.append(h_log)
                db.session.merge(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logging.getLogger('error_logger').exception(e)
                raise DatabaseException()
        else:
            logging.getLogger('logger').warning('Update operation warning. User not found.')
            raise UserException()

    @staticmethod
    def delete(users):
        try:
            for user in users:
                db.session.delete(user)
            db.session.commit()
            for user in users:
                path = 'Project/Server/DATA/' + user.home_catalog
                if os.path.isdir(path):
                    shutil.rmtree(path)
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get(user_id):
        try:
            return db.session.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get_all():
        try:
            return db.session.query(User).all()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
