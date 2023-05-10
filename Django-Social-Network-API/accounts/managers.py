from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
            self,
            email=None,
            username=None,
            password=None,
            **extra_fields
    ):
        if not email:
            return ValueError('Has not email')
        if not username:
            return ValueError('Has not username')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            username,
            password,
            **extra_fields
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
