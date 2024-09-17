from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os

Base = declarative_base()
DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))

class DataModel(Base):
    __tablename__ = 'processed_data'
    id = Column(Integer, primary_key=True)
    category = Column(String(50))
    value = Column(Float)
