# core/auth/helpers.py > Faisal
"""Contains helper functions"""

__all__ = [
    'OpenApi', 'open_api',
    'error_response',
    'is_username_available'
]

import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.decorators import permission_classes


def open_api(func):
    """Remove default permissions"""

    return permission_classes(())(func)


class OpenApi(APIView):
    """Remove default permissions"""

    permission_classes = ()
    authentication_classes = ()

    class Meta:
        abstract = True


def error_response(message, status_code=HTTP_400_BAD_REQUEST):
    return Response({
        'detail': message,
    }, status_code)


def is_username_available(username):
    """Checks if given username is available or not"""

    valid = bool(re.match(UnicodeUsernameValidator.regex, username))
    available = not get_user_model().objects.values('username').filter(username=username).exists()
    return valid and available
