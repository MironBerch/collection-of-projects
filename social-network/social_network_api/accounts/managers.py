from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for user model.
    """

    use_in_migrations = True

    def create_user(
            self,
            email: str = None,
            username: str = None,
            first_name: str = None,
            last_name: str = None,
            password: str = None,
            **extra_fields,
    ):
        """
        Function for creating user.
        """
        if not email:
            return ValueError('User must have an email address.')
        if not username:
            return ValueError('User must have an username.')
        if not first_name:
            return ValueError('User must have a first name.')
        if not last_name:
            return ValueError('User must have a last name.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email: str = None,
            username: str = None,
            first_name: str = None,
            last_name: str = None,
            password: str = None,
            **extra_fields,
    ):
        """
        Function for creating user with root permissions.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
