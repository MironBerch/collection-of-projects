from typing import Union

from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned

from accounts.models import User


class AuthenticationBackend(ModelBackend):
    def authenticate(
        self,
        request,
        email: Union[str, None] = None,
        password: Union[str, None] = None,
        **kwargs,
    ) -> Union[User, None]:
        """Override default authentication to allow for both email and
        username login.

        param email: Username or email address.
        param password: Password.
        """
        try:
            user = User.objects.get(
                Q(username=email) | Q(email__iexact=email)
            )
        except MultipleObjectsReturned:
            return (
                User.objects.filter(email=email).order_by('id').first()
            )
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
