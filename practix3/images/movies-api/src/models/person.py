from enum import Enum
from typing import ClassVar
from uuid import UUID

from models.base import OrjsonMixin, UUIDMixin


class RoleChoices(Enum):
    """Модель для соответствия названия поля в Elasticsearch и ролью персонала."""

    actors_names = 'actor'
    writers_names = 'writer'
    directors_names = 'director'


class BasePerson(UUIDMixin, OrjsonMixin):
    """Базовая модель персонала съемочной группы."""

    full_name: str

    class Config:
        populate_by_name = True


class Person(BasePerson):
    """Модель персонала съемочной группы."""

    role: str
    film_ids: list[UUID]


class PersonList(OrjsonMixin):
    """Модель списка персон с информацией об их ролях и фильмах."""

    persons: list[Person]
    item: ClassVar[type] = Person
