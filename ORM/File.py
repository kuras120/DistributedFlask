import hashlib

from ORM import db

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class File(db.Model):
    __tablename__ = "File"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    input_path = Column(String, nullable=False)
    output_path = Column(String, nullable=True)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))

    def __init__(self, name, description, login):
        self.name = name
        self.description = description
        self.input_path = hashlib.sha3_256(login.__str__().encode('utf-8')).hexdigest() + '/' + hashlib.\
            sha3_256(name.__str__().encode('utf-8')).hexdigest()
        self.added_on = datetime.now()

    def __repr__(self):
        return '<File %s>' % self.name
