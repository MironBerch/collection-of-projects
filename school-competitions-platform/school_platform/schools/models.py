from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Class(models.Model):
    school_class = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('класс'),
        primary_key=True,
    )

    year_of_study = models.SmallIntegerField(
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(11),
        ],
    )

    class_teacher = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='class_teacher',
        null=True,
    )

    class Meta:
        verbose_name = _('класс')
        verbose_name_plural = _('классы')

    def __str__(self):
        return self.school_class


class School(models.Model):
    school_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('название школы'),
    )
    is_current_school = models.BooleanField(
        verbose_name=_('текущая школа'),
        default=False,
    )

    class Meta:
        verbose_name = _('школа')
        verbose_name_plural = _('школы')

    def __str__(self):
        return self.school_name
