from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class AccountNotRegisteredException(APIException):
    status_code = 404
    default_detail = _('The account is not registered.')
    default_code = 'non-registered-account'


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = _('Wrong username or password.')
    default_code = 'invalid-credentials'
