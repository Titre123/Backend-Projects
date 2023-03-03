#!/usr/bin/env python3
""" Authentication module for the API.
"""


from typing import List, TypeVar, Any
from flask import request
from os import getenv


class Auth:
    """
        Auth class for user authentification
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Args:
                path -> str
                excluded_paths
            Return:
                False -> Bool
        """
        for pat in excluded_paths:
            if pat[len(pat)-1:] == '*' and pat[:len(pat)-1] in path:
                return False
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
            Args:
                request
            Return:
                None
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Args:
                Request
            Return:
                None
        """
        return None

    def session_cookie(self, request=None) -> Any:
        """
            Args:
                Request
            Return:
                None
        """
        session_id = getenv('SESSION_NAME', '_my_session_id')
        if request is None or session_id not in dict(request.cookies):
            return None
        return request.cookies.get(session_id)
