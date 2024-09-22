from typing import ClassVar

from models.base import OrjsonMixin, UUIDMixin


class BaseGenre(UUIDMixin):
    """Базовая модель жанра."""

    name: str

    class Config:
        populate_by_name = True


class Genre(BaseGenre):
    """Модель жанра."""

    description: str


class GenreList(OrjsonMixin):
    """Модель списка жанров."""

    genres: list[Genre]
    item: ClassVar[type] = Genre
