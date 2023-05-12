from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
            self,
            email=None,
            name=None,
            surname=None,
            patronymic=None,
            password=None,
            **extra_fields
        ):
        if not email:
            return ValueError('Почта обязательна')
        if not name:
            return ValueError('Имя обязательна')
        if not surname:
            return ValueError('Фамилия обязательна')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            surname=surname,
            patronymic=patronymic,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            name,
            surname,
            password,
            **extra_fields
        ):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            password=password
        )
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
