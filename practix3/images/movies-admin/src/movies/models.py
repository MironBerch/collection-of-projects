import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from movies.enums import FilmworkAccessType, FilmworkAgeRating, FilmworkType, PersonRole


class TimeStampedMixin(models.Model):
    """Абстрактый класс для отметки времени создания и модификации объектов модели."""

    created = models.DateTimeField(
        verbose_name='созданный',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name='модифицированный',
        auto_now=True,
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Абстрактый класс для генерации первичных ключей."""

    id = models.UUIDField(
        verbose_name='первичный ключ',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Жанр кинопроизведения."""

    name = models.CharField(
        verbose_name='название',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self) -> str:
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Кинопроизведение."""

    title = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    release_date = models.DateField(
        verbose_name='дата выпуска',
        null=True,
        blank=True,
        db_index=True,
    )
    rating = models.FloatField(
        verbose_name='рейтинг',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    access_type = models.CharField(
        verbose_name='тип доступа',
        max_length=31,
        choices=FilmworkAccessType.choices,
        default=FilmworkAccessType.PUBLIC,
    )
    type = models.CharField(
        verbose_name='тип кинопроизведения',
        max_length=31,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    age_rating = models.CharField(
        verbose_name='возрастной рейтинг',
        max_length=31,
        choices=FilmworkAgeRating.choices,
        default=FilmworkAgeRating.GENERAL,
    )
    genres = models.ManyToManyField(
        'Genre',
        verbose_name='связь между кинопроизведениями и жанрами',
        through='GenreFilmwork',
    )
    persons = models.ManyToManyField(
        'Person',
        verbose_name='связь между кинопроизведениями и персоналом съемочной группы',
        through='PersonFilmwork',
    )

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = 'кинопроизведение'
        verbose_name_plural = 'кинопроизведения'

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):
    """Промежуточная таблица привязки жанров и кинопроизведений."""

    film_work = models.ForeignKey(
        'Filmwork',
        verbose_name='кинопроизведение',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        'Genre',
        verbose_name='жанр',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name='созданный',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content\".\"genre_film_work'
        verbose_name = 'жанр кинопроизведения'
        verbose_name_plural = 'жанры кинопроизведений'
        unique_together = (
            ('film_work', 'genre'),
        )

    def __str__(self) -> str:
        return f'{self.film_work.title} - {self.genre.name}'


class Person(UUIDMixin, TimeStampedMixin):
    """Персонал съемочной группы (актер, режиссер и т.д.)."""

    full_name = models.TextField(
        verbose_name='фио',
        max_length=255,
    )

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = 'персонал съемочной группы'
        verbose_name_plural = 'персонал съемочных групп'

    def __str__(self) -> str:
        return self.full_name


class PersonFilmwork(UUIDMixin):
    """Промежуточная таблица для связи персонала и кинопроизведений."""

    film_work = models.ForeignKey(
        'Filmwork',
        verbose_name='кинопроизведение',
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        'Person',
        verbose_name='персонал',
        on_delete=models.CASCADE,
    )
    role = models.TextField(
        verbose_name='роль',
        choices=PersonRole.choices,
        default=PersonRole.ACTOR,
    )
    created = models.DateTimeField(
        verbose_name='созданный',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content\".\"person_film_work'
        verbose_name = 'персонал съемочной группы кинопроизведения'
        verbose_name_plural = 'персонал съемочной группы кинопроизведений'
        index_together = (
            ('film_work', 'person'),
        )

    def __str__(self) -> str:
        return f'{self.film_work.title} - {self.person.full_name} - {self.role}'
