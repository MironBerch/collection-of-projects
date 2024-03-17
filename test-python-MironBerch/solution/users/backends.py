from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned

from users.models import User


class AuthenticationBackend(ModelBackend):
    def authenticate(
        self,
        request,
        login: str | None = None,
        password: str | None = None,
        **kwargs,
    ) -> User | None:
        try:
            user = User.objects.get(login=login)
        except MultipleObjectsReturned:
            return (
                User.objects.filter(login=login).order_by('id').first()
            )
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
