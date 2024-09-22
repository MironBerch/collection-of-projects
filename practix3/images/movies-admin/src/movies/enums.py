from django.db import models


class FilmworkType(models.TextChoices):
    """Тип кинопроизведения."""

    MOVIE = 'movie', 'фильм'
    TV_SHOW = 'tv_show', 'тв шоу'


class FilmworkAgeRating(models.TextChoices):
    """Возрастной рейтинг кинопроизведения."""

    GENERAL = 'G', 'G: Основная аудитория'
    PARENTAL_GUIDANCE = 'PG', 'PG: Предлагается родительский контроль'
    PARENTS = 'PG-13', 'PG-13: Родители предупредили'
    RESTRICTED = 'R', 'R: Ограниченный'
    ADULTS = 'NC-17', 'NC-17: Только для взрослых'


class FilmworkAccessType(models.TextChoices):
    """Тип доступа к кинопроизведению (бесплатный, только для подписчиков)."""

    PUBLIC = 'public', 'общественный'
    SUBSCRIPTION = 'subscription', 'подписка'


class PersonRole(models.TextChoices):
    """Роль участника."""

    ACTOR = 'actor', 'актёр'
    DIRECTOR = 'director', 'режиссёр'
    WRITER = 'writer', 'сценарист'
