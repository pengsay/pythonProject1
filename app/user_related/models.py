from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date,PickleType
from database.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(128))
    principals = Column(String(256),default='[]')