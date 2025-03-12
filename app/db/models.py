from sqlalchemy import Integer,String,Column
from .database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String,unique=True)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Integer, default=True)