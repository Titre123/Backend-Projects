#!/usr/bin/env python3
""" Basic Authentication module for the API.
"""


from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth
import base64
import hashlib
from models.user import User


def isBase64(s):
    '''
        Check if string is base64 string
    '''
    try:
        return base64.b64encode(base64.b64decode(s)).decode('utf-8') == s
    except Exception:
        return False


class BasicAuth(Auth):
    """
        Basic Autnentification class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''
            Args:
                authorization_header: str
            Return:
                str
        '''
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header.split()[0] != "Basic":
            return None
        else:
            return ' '.join(authorization_header.split()[1:])

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        '''
            Args:
                base64_authorization_header: str
            Return:
                str
        '''
        type_str = type(base64_authorization_header)
        authen = base64_authorization_header
        if authen is None or type_str != str or isBase64(authen) is False:
            return None
        else:
            return base64.b64decode(authen).decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''
            Args:
                decoded_base64_authorization_header: str
            Return:
                tuple -> (str, str)
        '''
        authen = decoded_base64_authorization_header
        if authen is None or type(authen) != str:
            return (None, None)
        if ':' not in [*decoded_base64_authorization_header]:
            return (None, None)
        else:
            decode_array = [*decoded_base64_authorization_header]
            ind = decode_array.index(':')
            email = ''.join(decode_array[:ind])
            password = ''.join(decode_array[ind+1:])
            return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''
            get user from credentials
        '''
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) != str or type(user_pwd) != str:
            return None
        try:
            all_user = User.all()
            if all_user:
                user_list = User.search({'email': user_email})
                lib = hashlib.sha256(user_pwd.encode()).hexdigest().lower()
                if len(user_list) > 0 and lib == user_list[0].password:
                    return user_list[0]
                else:
                    return None
        except KeyError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Args:
                Request
            Return:
                None
        """
        authorize = self.authorization_header(request)
        extract_base64 = self.extract_base64_authorization_header(authorize)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        extract_user_credentials = self.extract_user_credentials(decode_base64)
        user_email = extract_user_credentials[0]
        user_pwd = extract_user_credentials[1]
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
