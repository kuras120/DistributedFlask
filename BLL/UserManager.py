import uuid
import logging
import hashlib

from ORM.User import User
from ORM.DbConfig import db_session


class UserManager:
    def __init__(self):
        self.__logger = logging.getLogger('logger')

    @staticmethod
    def add_user(login, password):
        new_user = None
        if not db_session.query(User).filter(User.login == login).first():
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password.encode("utf-8") + salt.encode("utf-8")).hexdigest()
            new_user = User(login=login, hashed_password=hashed_password, salt=salt)
            db_session.add(new_user)
            db_session.commit()
        return new_user

    @staticmethod
    def check_user(login, password):
        user = db_session.query(User).filter(User.login == login).first()
        if user:
            hash_password = hashlib.sha512(password.encode('utf-8') + user.salt.encode('utf-8')).hexdigest()
            if user.hashed_password == hash_password:
                return user
            else:
                raise Exception("Wrong password.")
        else:
            raise Exception("Cannot find user.")
