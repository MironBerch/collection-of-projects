import datetime

from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    token = models.CharField(max_length=255)
    user_id = models.PositiveIntegerField()
    black = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id


class UserManager(BaseUserManager):
    """Менеджер пользовательской модели `User`."""

    use_in_migrations = True

    def create_user(
            self,
            email: str,
            login: str,
            password: str = None,
            **extra_fields,
    ):
        user = self.model(
            email=self.normalize_email(email),
            login=login,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользовательская модель `User`."""

    login = models.CharField(
        verbose_name=_('имя'),
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        verbose_name=_('почта'),
        max_length=50,
        unique=True,
    )
    country_code = models.CharField(
        max_length=2,
    )
    phone = PhoneNumberField(
        verbose_name=_('номер телефона'),
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+\d{9,}$',
                message='Номер телефона необходимо ввести в формате: +XXXXXXXXXXXXX.',
            )
        ],
    )
    image = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(
        verbose_name=_('активный'),
        default=True,
    )
    is_public = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'login'

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return f'{self.login}'


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_friend')
    addedAt = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.addedAt:
            self.addedAt = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        super(Friend, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.friend}'
