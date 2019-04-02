import secrets
import hashlib
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from ORM.DbConfig import Base


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __init__(self, login, password):
        self.login = login
        self.salt = secrets.token_hex(8)
        self.hashed_password = hashlib.sha512(password.encode("utf-8") + self.salt.encode("utf-8")).hexdigest()
        self.created_on = datetime.now()
        self.last_login = None

    def __repr__(self):
        return '<User %s>' % self.login
