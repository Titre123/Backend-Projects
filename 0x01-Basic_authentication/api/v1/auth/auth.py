#!/usr/bin/env python3
""" Authentication module for the API.
"""


from typing import List, TypeVar
from flask import request


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
