from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """

    email = models.EmailField(
        _('email address'),
        max_length=100,
        unique=True,
        null=True,
    )
    username = models.CharField(
        _('username'),
        max_length=100,
        unique=True,
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
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


def get_default_profile_image() -> str:
    return 'default/default_profile_image.png'


def get_default_profile_banner() -> str:
    return 'default/default_profile_banner.png'


def get_profile_image_upload_path(instance: 'Profile', filename: str) -> str:
    return f'upload/users/{instance.user.email}/profile_image/{filename}'


def get_profile_banner_upload_path(instance: 'Profile', filename: str) -> str:
    return f'upload/users/{instance.user.email}/profile_banner/{filename}'


class ProfileGenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'


class Profile(models.Model):
    """
    Profile for user.
    """

    user: User = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    profile_image = models.ImageField(
        verbose_name='user profile image',
        blank=True,
        null=True,
        upload_to=get_profile_image_upload_path,
        default=get_default_profile_image,
    )
    profile_banner = models.ImageField(
        verbose_name='user profile banner',
        blank=True,
        null=True,
        upload_to=get_profile_banner_upload_path,
        default=get_default_profile_banner,
    )
    gender = models.CharField(
        verbose_name='user gender',
        blank=True,
        max_length=2,
        choices=ProfileGenderChoices.choices,
    )
    description = models.TextField(
        verbose_name='user profile description',
        blank=True,
        max_length=500,
    )

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return f'Profile for {self.user}'
