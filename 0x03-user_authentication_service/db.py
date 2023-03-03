#!/usr/bin/env python3
"""DB module
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
            Add new user to the database
        '''
        try:
            self.__session = self._session
            new_user = User(email=email, hashed_password=hashed_password)
            self.__session.add(new_user)
            self.__session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''
            Search for th user queried
        '''
        try:
            user = self.__session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except AttributeError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
            Update the user that is has the user_id
        '''
        try:
            user = self.find_user_by(id=user_id)
            key = list(kwargs.keys())[0]
            if getattr(user, key):
                setattr(user, key, kwargs[key])
                self.__session.commit()
            if key == 'session_id' or key == 'reset_token':
                setattr(user, key, kwargs[key])
                self.__session.commit()
        except AttributeError:
            raise ValueError
