from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned

User = get_user_model()


class AuthenticationBackend(ModelBackend):
    """
    User authentication backend.
    Authenticate user by suitable credentials.
    """

    def authenticate(self, request, credentials=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=credentials) | Q(email__iexact=credentials)
            )
        except MultipleObjectsReturned:
            return (
                User.objects.filter(email=credentials).order_by('id').first()
            )
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
