from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ORM.DbConfig import Base


class Data(Base):
    __tablename__ = "Data"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sub_name = Column(String, nullable=True)
    key = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User")
