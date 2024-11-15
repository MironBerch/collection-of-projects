from typing import ClassVar, Type
from uuid import UUID

from pydantic import BaseModel

from models.base import OrjsonMixin, UUIDMixin


class FilmworkGenre(BaseModel):
    """Модель жанра в кинопроизведении."""

    uuid: UUID
    name: str

    class Config(OrjsonMixin.Config):
        allow_population_by_field_name = True


class FilmworkPerson(BaseModel):
    """Модель персоны в кинопроизведении."""

    uuid: UUID
    full_name: str

    class Config(OrjsonMixin.Config):
        allow_population_by_field_name = True


class Filmwork(UUIDMixin, OrjsonMixin):
    """Модель кинопроизведения."""

    title: str
    rating: float
    description: str
    genre: list[FilmworkGenre]
    actors: list[FilmworkPerson]
    writers: list[FilmworkPerson]
    directors: list[FilmworkPerson]


class FilmworkModified(UUIDMixin, OrjsonMixin):
    """Модель кинопроизведения с краткой информацией."""

    title: str
    imdb_rating: float


class FilmworkList(OrjsonMixin):
    """Модель списка кинопроизведений с краткой информацией."""

    __root__: list[FilmworkModified]
    item: ClassVar[Type] = FilmworkModified
