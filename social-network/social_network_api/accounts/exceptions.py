from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class AccountDoesNotExistException(APIException):
    status_code = 404
    default_detail = _('This account does not exist.')
    default_code = 'account-does-not-exist'


class ProfileDoesNotExistException(APIException):
    status_code = 404
    default_detail = _('This profile does not exist.')
    default_code = 'profile-does-not-exist'
