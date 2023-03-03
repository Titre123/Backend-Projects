#!/usr/bin/env python3
'''
    User Model Using SqlAlchelmy
'''


import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# declare base from Models
Base = declarative_base()


class User(Base):
    '''
        Class User inheriting from Base
        It create User Models
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=True)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
