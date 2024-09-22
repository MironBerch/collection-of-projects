from django.db import models
from django.utils.translation import gettext_lazy as _


class FilmworkType(models.TextChoices):
    """Тип кинопроизведения."""

    MOVIE = 'MV', _('Фильм')
    TV_SHOW = 'TV', _('ТВ шоу')


class FilmworkAgeRating(models.TextChoices):
    """Возрастной рейтинг кинопроизведения."""

    GENERAL = 'G', _('G: Основная аудитория')
    PARENTAL_GUIDANCE = 'PG', _('PG: Предлагается родительский контроль')
    PARENTS = 'PG-13', _('PG-13: Родители предупредили')
    RESTRICTED = 'R', _('R: Ограниченный')
    ADULTS = 'NC-17', _('NC-17: Только для взрослых')


class FilmworkAccessType(models.TextChoices):
    """Тип доступа к кинопроизведению (бесплатный, только для подписчиков и т.д.)."""

    PUBLIC = 'public', _('Общественный')
    SUBSCRIPTION = 'subscription', _('Подписка')


class PersonRole(models.TextChoices):
    """Роль участника."""

    ACTOR = 'actor', _('актер')
    DIRECTOR = 'director', _('директор')
    WRITER = 'writer', _('писатель')
