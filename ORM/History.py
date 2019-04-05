from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ORM import db
from enum import Enum


class TypeH(Enum):
    Info = 0
    Warning = 1
    Error = 2


class History(db.Model):
    __tablename__ = "History"
    id = Column(Integer, primary_key=True)
    type_h = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User")

    def __init__(self, type_h, description, user_id):
        self.type = type_h
        self.description = description
        self.added_on = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<%s: %s>' % (self.type_h, self.description)
