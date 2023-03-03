#!/usr/bin/env python3
"""Auth module
"""


import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    '''
        hash password
    '''
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    '''
        generate uuid for session id
    '''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
            register a new user to the database
        '''
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))

        except (AttributeError, InvalidRequestError):
            hashed_password = _hash_password(password)
            self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        '''
        '''
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except (AttributeError, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        '''
            create a new session and update a user session_id
        '''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (AttributeError, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
            get a user using the session
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (AttributeError, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        '''
            destroy a session
        '''
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        '''
        '''
        try:
            user = self._db.find_user_by(email=email)
            token = uuid.uuid4()
            self._db.update_user(reset_token=token)
            return token
        except (AttributeError, InvalidRequestError, NoResultFound):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(hashed_password=hashed_password)
            self.__db.update_password(reset_token=None)
        except (AttributeError, InvalidRequestError, NoResultFound):
            raise ValueError