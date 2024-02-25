import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        verbose_name=_('созданный'),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_('модифицированный'),
        auto_now=True,
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Жанр фильма."""

    name = models.CharField(
        verbose_name=_('название'),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('описание'),
        blank=True,
    )

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')

    def __str__(self) -> str:
        return self.name


class FilmworkType(models.TextChoices):
    """Тип фильма."""

    MOVIE = 'MV', _('Фильм')
    TV_SHOW = 'TV', _('ТВ шоу')


class FilmworkAgeRating(models.TextChoices):
    """Возрастной рейтинг фильма."""

    GENERAL = 'G', _('G: Основная аудитория')
    PARENTAL_GUIDANCE = 'PG', _('PG: Предлагается родительский контроль')
    PARENTS = 'PG-13', _('PG-13: Родители предупредили')
    RESTRICTED = 'R', _('R: Ограниченный')
    ADULTS = 'NC-17', _('NC-17: Только для взрослых')


class FilmworkAccessType(models.TextChoices):
    """Тип доступа к фильму (бесплатный, только для подписчиков и т.д.)."""

    PUBLIC = 'public', _('Общественный')
    SUBSCRIPTION = 'subscription', _('Подписка')


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Фильм."""

    title = models.CharField(
        verbose_name=_('название'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('описание'),
        blank=True,
    )
    release_date = models.DateField(
        verbose_name=_('дата выпуска'),
        null=True,
        blank=True,
        db_index=True,
    )
    rating = models.FloatField(
        verbose_name=_('рейтинг'),
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    access_type = models.CharField(
        _('тип доступа'),
        max_length=31,
        choices=FilmworkAccessType.choices,
        default=FilmworkAccessType.PUBLIC,
    )
    type = models.CharField(
        _('тип фильма'),
        max_length=2,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    age_rating = models.CharField(
        _('возрастной рейтинг'),
        max_length=31,
        choices=FilmworkAgeRating.choices,
        default=FilmworkAgeRating.GENERAL,
    )
    file_path = models.FileField(
        verbose_name=_('файл'),
        blank=True,
        null=True,
        upload_to='movies/',
    )
    genres = models.ManyToManyField(
        'Genre',
        through='GenreFilmwork',
    )
    persons = models.ManyToManyField(
        'Person',
        through='PersonFilmwork',
    )

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('фильм')
        verbose_name_plural = _('фильмы')

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):
    """Промежуточная таблица привязки жанров и фильмов."""

    film_work = models.ForeignKey(
        'Filmwork',
        verbose_name=_('фильм'),
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        'Genre',
        verbose_name=_('жанр'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name=_('созданный'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content\".\"genre_film_work'
        verbose_name = _('жанр фильма')
        verbose_name_plural = _('жанры фильмов')
        unique_together = (
            ('film_work', 'genre'),
        )

    def __str__(self) -> str:
        return f'{self.film_work.title} - {self.genre.name}'


class Person(UUIDMixin, TimeStampedMixin):
    """Персонал съемочной группы (актер, режиссер и т.д.)."""

    full_name = models.TextField(
        verbose_name=_('full name'),
        max_length=255,
    )

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('участник съемочной группы')
        verbose_name_plural = _('участники съемочной группы')

    def __str__(self) -> str:
        return self.full_name


class PersonRole(models.TextChoices):
    """Роль участника."""

    ACTOR = 'actor', _('актер')
    DIRECTOR = 'director', _('директор')
    WRITER = 'writer', _('писатель')


class PersonFilmwork(UUIDMixin):
    """Промежуточная таблица для связи персонала и фильмов."""

    film_work = models.ForeignKey(
        'Filmwork',
        verbose_name=_('фильм'),
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        'Person',
        verbose_name=_('участник'),
        on_delete=models.CASCADE,
    )
    role = models.TextField(
        verbose_name=_('роль'),
        choices=PersonRole.choices,
        default=PersonRole.ACTOR,
    )
    created = models.DateTimeField(
        verbose_name=_('созданный'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content\".\"person_film_work'
        verbose_name = _('участник съемочной группы фильма')
        verbose_name_plural = _('участники съемочной группы фильма')
        index_together = (
            ('film_work', 'person'),
        )

    def __str__(self) -> str:
        return f'{self.film_work.title} - {self.person.full_name} - {self.role}'
