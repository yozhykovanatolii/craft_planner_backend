from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)

class User(Base):
    __tablename__ = 'users'
    
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    avatar_url = Column(String, nullable=False)