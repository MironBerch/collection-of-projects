from enum import Enum
from typing import ClassVar
from uuid import UUID

from models.base import OrjsonMixin, UUIDMixin


class RoleChoices(Enum):
    """Перечисление для определения ролей."""

    actors_names = 'actor'
    writers_names = 'writer'
    director = 'director'


class Person(UUIDMixin, OrjsonMixin):
    """Модель персоны."""

    full_name: str
    role: str
    film_ids: list[UUID]


class PersonList(OrjsonMixin):
    """Модель списка персон с информацией об их ролях и кинопроизведениях."""

    __root__: list[Person]
    item: ClassVar[type] = Person
