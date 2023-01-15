from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class CustomBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None