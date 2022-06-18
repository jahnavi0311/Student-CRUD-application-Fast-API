from sqlalchemy import Column, Integer, String
from database import Base

# Define StuDent class inheriting from Base
class StuDent(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    sname = Column(String(256))
    section = Column(String(32))
    grp = Column(String(32))
