from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {'reason': 'Problems with authentication, you have problems with token.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return None
