import os
import hashlib

from ORM import db

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class File(db.Model):
    __tablename__ = "File"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    input_path = Column(String, nullable=False)
    output_path = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))

    def __init__(self, name, user_catalog, description=None):
        self.name = name
        self.description = description
        self.input_path = user_catalog + '/INPUT/'
        self.output_path = user_catalog + '/OUTPUT/'
        self.added_on = datetime.now()

    def __repr__(self):
        return '<File %s>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}