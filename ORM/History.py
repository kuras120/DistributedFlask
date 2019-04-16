import enum
from ORM import db
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum


class TypeH(enum.Enum):
    Info = 'Info'
    Warning = 'Warning'
    Error = 'Error'


class History(db.Model):
    __tablename__ = "History"
    id = Column(Integer, primary_key=True)
    type_h = Column(Enum(TypeH), nullable=False)
    description = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))

    def __init__(self, type_h, description):
        self.type_h = type_h
        self.description = description
        self.added_on = datetime.now()

    def __repr__(self):
        return '<%s: %s>' % (self.type_h, self.description)
