from typing import ClassVar

from models.base import UUIDMixin


class Genre(UUIDMixin):
    """Класс для валидации данных `genre`."""

    name: str
    description: str
    _index: ClassVar[str] = 'genres'
