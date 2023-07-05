import phonenumbers
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from phonenumbers.phonenumberutil import NumberParseException


class PhoneNumberAuthenticationBackend(ModelBackend):
    """
    User authentication backend.
    For authentication using user phone number.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            number = phonenumbers.parse(
                username,
                settings.PHONENUMBER_DEFAULT_REGION
            )
            if not phonenumbers.is_valid_number(number):
                return None
            try:
                user = User.objects.get(phone__phone_number=number)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        except NumberParseException:
            return None
