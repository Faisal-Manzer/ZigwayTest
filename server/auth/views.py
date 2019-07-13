# auth/views.py > Faisal
__all__ = ['SignInView', 'TokenRefreshView', 'is_username_available', 'CreateUserView']

from django.contrib.auth import authenticate
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings

from .serializers import UserSerializer

from auth.helpers import (
    OpenApi, open_api,
    error_response,
    is_username_available as username_check
)

from auth.serializers import SignINViewSerializer

"""
SignInView and TokenRefreshView are their just to add 'expires' (expiring time) to response.
"""


class SignInView(OpenApi):
    """Check user credentials and generate proper error message,
    If credentials are right then send JWT Token

    post
        username
        password
    """
    user = None
    serializer_class = SignINViewSerializer

    def post(self, request, username=None, password=None):

        try:
            username = username or request.data['username']
            password = password or request.data['password']

        except MultiValueDictKeyError:
            # Just for a check, Will never happen from API
            return error_response('Request should contain valid parameters')
        except KeyError:
            return error_response('Either password or username not provided')

        if not get_user_model().objects.filter(username=username).exists():
            return error_response(f'Username {username} does not exist')

        # Check for credentials
        # Will not Sign IN from this
        self.user = authenticate(username=username, password=password)

        if self.user is not None:
            refresh = RefreshToken.for_user(self.user)
            access_token = refresh.access_token

            return Response({
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'expires': access_token.payload['exp']
                },
                'user': {
                    'username': self.user.username,
                    'name': self.user.get_full_name(),
                    'email': self.user.email,
                }
            })
        else:
            return error_response('No active account found with the given credentials')


class TokenRefreshView(TokenViewBase):
    """
    Overrides rest_framework_simplejwt.views.TokenRefreshView

    post
        refresh
    """

    class TokenRefreshSerializer(serializers.Serializer):
        """
        Override for rest_framework_simplejwt.serializers.TokenRefreshSerializer
        """

        refresh = serializers.CharField()

        def validate(self, attrs):
            refresh = RefreshToken(attrs['refresh'])

            data = {
                'access': str(refresh.access_token),

                # This field has been added
                # This was an necessary override to insure simple experience
                'expires': refresh.access_token.payload['exp']
            }

            if api_settings.ROTATE_REFRESH_TOKENS:
                if api_settings.BLACKLIST_AFTER_ROTATION:
                    try:
                        # Attempt to blacklist the given refresh token
                        refresh.blacklist()
                    except AttributeError:
                        # If blacklist app not installed, `blacklist` method will
                        # not be present
                        pass

                refresh.set_jti()
                refresh.set_exp()

                data['refresh'] = str(refresh)

            return data

    # Set the new serializer class
    serializer_class = TokenRefreshSerializer


@api_view(['GET'])
@open_api
def is_username_available(request):
    """Checks if given username is available or not

    get
        username
    """

    try:
        username = request.query_params['username']
        return Response({
            'username': username,
            'available': username_check(username),
        })

    except KeyError:
        """If 'username' is not available in query_params"""
        return error_response('Provide valid arguments')


class CreateUserView(OpenApi, CreateAPIView):
    """Serializer to create new user"""

    model = get_user_model()
    serializer_class = UserSerializer
