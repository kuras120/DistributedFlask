from datetime import datetime

from Project.Server.ORM import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class File(db.Model):
    __tablename__ = "Files"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))

    def __init__(self, name):
        self.name = name
        self.added_on = datetime.now().replace(microsecond=0)

    def __repr__(self):
        return '<File %s>' % self.name
