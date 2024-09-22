from fastapi import APIRouter

from models.movie import BaseFilm, FilmList
from models.person import Person, PersonList

router = APIRouter(tags=['persons'])


@router.get(
    '/persons',
    response_model=PersonList,
    summary='Персоны',
    description='Список персон',
    response_description='Полное имя, основная роль, фильмы c участием персоны',
)
async def persons() -> list[Person]:
    pass


@router.get(
    '/persons/search',
    response_model=PersonList,
    summary='Поиск персон',
    description='Полнотекстовый поиск по именам персон',
    response_description='Полное имя, основная роль, фильмы c участием персоны',
)
async def persons_search() -> list[Person]:
    pass


@router.get(
    '/persons/{person_id}',
    response_model=Person,
    summary='Страница персоны',
    description='Полная информация по персоне',
    response_description='Полное имя, основная роль, фильмы c участием персоны',
)
async def person_pk() -> Person:
    pass


@router.get(
    '/persons/{person_id}/film',
    response_model=FilmList,
    summary='Фильмы по персоне',
    description='Фильмы персоны отсортированные по популярности',
    response_description='Название и рейтинг фильмов персоны',
)
async def person_by_pk_films() -> list[BaseFilm]:
    pass
