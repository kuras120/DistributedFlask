import logging

from ORM import db
from ORM.User import User
from ORM.File import File
from ORM.History import History, TypeH

from Utilities.CustomExceptions import UserException, DatabaseException


class UserDAO:
    @staticmethod
    def create(type_h, description, user):
        try:
            log_h = History(type_h=type_h, description=description)
            user.history.append(log_h)
            db.session.merge(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def read(user_id, type_h=None):
        try:
            if type_h:
                return db.session.query(History).filter(History.type_h == type_h, History.user_id == user_id).all()
            else:
                return db.session.query(History).filter(History.user_id == user_id).all()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def update():
        raise NotImplementedError

    @staticmethod
    def delete(history):
        try:
            for log in history:
                db.session.delete(log)
            db.session.commit()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get(history_id):
        try:
            return db.session.query(History).filter(History.id == history_id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get_all(user_id):
        try:
            return db.session.query(History).filter(History.user_id == user_id).all()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
