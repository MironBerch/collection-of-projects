import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
    )
    modified = models.DateTimeField(
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
    """Film genre."""

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class FilmworkType(models.TextChoices):
    """Film type."""

    MOVIE = 'MV', _('Film')
    TV_SHOW = 'TV', _('TV show')


class FilmworkAgeRatingChoices(models.TextChoices):
    """Film age rating.

    List of possible age ratings:
    Rated G: General audiences.
    Rated PG: Parental guidance suggested.
    Rated PG-13: Parents strongly cautioned.
    Rated R: Restricted.
    Rated NC-17: Adults Only.
    """

    GENERAL = 'G', _('G: General audience')
    PARENTAL_GUIDANCE = 'PG', _('PG: Parental guidance suggested')
    PARENTS = 'PG-13', _('PG-13: Parents cautioned')
    RESTRICTED = 'R', _('R: Restricted')
    ADULTS = 'NC-17', _('NC-17: Adults only')


class FilmworkAccessTypeChoices(models.TextChoices):
    """Film access type (free, only for subscribers, etc.)."""

    PUBLIC = 'public', _('Public')
    SUBSCRIPTION = 'subscription', _('Subscription')


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Film."""

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )
    release_date = models.DateField(
        verbose_name=_('release date'),
        null=True,
        blank=True,
        db_index=True,
    )
    rating = models.FloatField(
        verbose_name=_('rating'),
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    access_type = models.CharField(
        verbose_name=_('access type'),
        max_length=31,
        choices=FilmworkAccessTypeChoices.choices,
        default=FilmworkAccessTypeChoices.PUBLIC,
    )
    type = models.CharField(
        verbose_name=_("film's type"),
        max_length=2,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    age_rating = models.CharField(
        verbose_name=_('age rating'),
        max_length=31,
        choices=FilmworkAgeRatingChoices.choices,
        default=FilmworkAgeRatingChoices.GENERAL,
    )
    file_path = models.FileField(
        verbose_name=_('file'),
        blank=True,
        null=True,
        upload_to='movies/',
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmwork',
    )
    persons = models.ManyToManyField(
        'Person',
        through='PersonFilmwork',
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    """Intermediate table for linking genres and films."""

    film_work = models.ForeignKey(
        Filmwork,
        verbose_name=_('film'),
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        'Genre',
        verbose_name=_('genre'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _("film's genre")
        verbose_name_plural = _("film's genres")
        unique_together = (
            (
                'film_work',
                'genre',
            ),
        )

    def __str__(self):
        return f'{self.film_work}'


class Person(UUIDMixin, TimeStampedMixin):
    """Member of a film crew (actor, director, etc.)."""

    full_name = models.TextField(
        _('full name'),
        max_length=255,
    )

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('crew member')
        verbose_name_plural = _('crew members')

    def __str__(self):
        return self.full_name


class PersonRoleChoices(models.TextChoices):
    """Person role."""

    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')


class PersonFilmwork(UUIDMixin):
    """Intermediate table for linking persons and films."""

    film_work = models.ForeignKey(
        Filmwork,
        verbose_name=_('film'),
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        Person,
        verbose_name=_('crew member'),
        on_delete=models.CASCADE,
    )
    role = models.TextField(
        verbose_name=_('role'),
        choices=PersonRoleChoices.choices,
        default=PersonRoleChoices.ACTOR,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('film crew member')
        verbose_name_plural = _('film crew members')
        index_together = (
            (
                'film_work',
                'person',
            ),
        )

    def __str__(self):
        return f'{self.film_work}'
