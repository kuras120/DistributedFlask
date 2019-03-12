from sqlalchemy import Column, Integer, String

from ORM.DbConfig import Base


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    def __init__(self, login=None, hashed_password=None, salt=None):
        self.login = login
        self.hashed_password = hashed_password
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % self.login
