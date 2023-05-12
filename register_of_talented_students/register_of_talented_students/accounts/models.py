from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=100,
        unique=True,
        null=True,
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    surname = models.CharField(
        _('surname'),
        max_length=100,
    )
    patronymic = models.CharField(
        _('patronymic'),
        max_length=100,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        _('active'),
        default=False,
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
    )
    is_superuser = models.BooleanField(
        _('superuser'),
        default=False,
    )
    is_staff = models.BooleanField(
        _('staff'),
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
