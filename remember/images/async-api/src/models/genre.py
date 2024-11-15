from typing import ClassVar

from models.base import OrjsonMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonMixin):
    """Модель жанра фильма."""

    name: str
    description: str


class GenreList(OrjsonMixin):
    """Поле (атрибут) списка жанров."""

    __root__: list[Genre]
    item: ClassVar[type] = Genre
