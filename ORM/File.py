from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ORM import db


class File(db.Model):
    __tablename__ = "Data"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    input_path = Column(String, nullable=False)
    output_path = Column(String, nullable=True)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User")

    def __init__(self, name, description, input_path, user_id):
        self.name = name
        self.description = description
        self.input_path = input_path
        self.added_on = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<File %s>' % self.name
