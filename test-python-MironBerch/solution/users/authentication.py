from datetime import datetime, timezone

import jwt
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication

from django.conf import settings

from users.models import User
from users.services import secure_that_good_token


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = None
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise exceptions.AuthenticationFailed(
                'No authorization_header',
                code=status.HTTP_401_UNAUTHORIZED,
            )
        if authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
        else:
            raise exceptions.AuthenticationFailed(
                'Token was not in correct format',
                code=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            exp_timestamp = payload.get('exp')
            if exp_timestamp is None or exp_timestamp < datetime.now(timezone.utc).timestamp():
                raise exceptions.AuthenticationFailed(
                    'Token has expired',
                    code=status.HTTP_401_UNAUTHORIZED,
                )
            user_id = payload.get('user_id')
            if not secure_that_good_token(pk=user_id, token=token):
                raise exceptions.AuthenticationFailed(
                    'Black token',
                    code=status.HTTP_401_UNAUTHORIZED,
                )
            user = User.objects.get(id=user_id)
            return (user, None)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed(
                'Token is not valid',
                code=status.HTTP_401_UNAUTHORIZED,
            )
