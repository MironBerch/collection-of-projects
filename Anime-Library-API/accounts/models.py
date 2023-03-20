from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=60,
        unique=True,
    )
    email = models.EmailField(
        _('email'),
        max_length=60,
        unique=True,
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now
    )

    is_email_confirmed = models.BooleanField(
        _('is_email_confirmed'),
        default=False,
        help_text=_('Shows if the user email is verified.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Determines if the user can using site.'),
    )
    is_superuser = models.BooleanField(
        _('superuser'),
        default=False,
        help_text=_('Determines if the user can using administrative rights on the site.'),
    )
    is_staff = models.BooleanField(
        _('staff'),
        default=False,
        help_text=_('Determines if the user can log into the admin panel.'),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class EmailConfirmMessage(models.Model):
    """Model of email confirm message"""
    
    code = models.CharField(
        verbose_name='8 digits email confirm code',
        max_length=8,
    )
    email = models.CharField(
        max_length=60,
    )
    dispatch_time = models.DateTimeField(
        auto_now_add=True,
    )