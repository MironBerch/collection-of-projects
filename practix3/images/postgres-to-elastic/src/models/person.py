from typing import ClassVar

from models.base import UUIDMixin


class Person(UUIDMixin):
    """Класс для валидации данных `person`."""

    full_name: str
    _index: ClassVar[str] = 'persons'

    class Config(object):
        populate_by_name = True
