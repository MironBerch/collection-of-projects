from model_utils import FieldTracker

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import ActivatedAccountsManager, UserManager
from school.models import Class


class User(AbstractBaseUser, PermissionsMixin):
    """Custom `User` model."""

    profile: 'Profile'
    username = None
    email = models.EmailField(
        verbose_name=_('почта'),
        max_length=60,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_('имя'),
        max_length=30,
    )
    surname = models.CharField(
        verbose_name=_('фамилия'),
        max_length=30,
    )
    patronymic = models.CharField(
        verbose_name=_('отчество'),
        max_length=30,
        blank=True,
    )

    date_joined = models.DateTimeField(
        verbose_name=_('дата присоединения'),
        auto_now_add=True,
    )
    last_login = models.DateTimeField(
        verbose_name=_('последний вход в систему'),
        auto_now=True,
    )

    class RoleChoices(models.TextChoices):
        STUDENT = 'ученик', 'ученик'
        TEACHER = 'учитель', 'учитель'

    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        verbose_name=_('роль'),
        default=RoleChoices.STUDENT,
    )

    is_email_confirmed = models.BooleanField(
        verbose_name=_('электронная почта подтверждена'),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('активный'),
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_('персонал'),
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name=_('суперпользователь'),
        default=False,
    )

    objects = UserManager()
    activated = ActivatedAccountsManager()

    # login parameter
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    # email field tracker
    email_tracker = FieldTracker(fields=['email'])

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return f'{self.surname} {self.name}'

    @property
    def full_name(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Profile(models.Model):
    """Profile for `User`."""

    date_of_birth = models.DateField(
        verbose_name=_('дата рождения'),
        blank=True,
        null=True,
    )

    school_class = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        verbose_name=_('класс'),
        blank=True,
        null=True,
    )

    user: User = models.OneToOneField(
        User,
        verbose_name=_('пользователь'),
        related_name='profile',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')

    def __str__(self):
        return f'Профиль {self.user}'
