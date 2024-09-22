from typing import ClassVar, Type

from models.base import OrjsonMixin, UUIDMixin
from models.genre import BaseGenre
from models.person import BasePerson


class BaseFilm(UUIDMixin, OrjsonMixin):
    """Базовая модель кинопроизведения."""

    title: str
    rating: float


class Film(BaseFilm):
    """Модель кинопроизведения."""

    title: str
    rating: int
    description: str
    genres: list[BaseGenre]
    actors: list[BasePerson]
    writers: list[BasePerson]
    directors: list[BasePerson]


class FilmList(OrjsonMixin):
    """Модель списка фильмов с краткой информацией."""

    movies: list[BaseFilm]
    item: ClassVar[Type] = BaseFilm
