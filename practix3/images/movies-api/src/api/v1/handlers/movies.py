from fastapi import APIRouter

from models.movie import BaseFilm, Film, FilmList

router = APIRouter(tags=['movies'])


@router.get(
    '/films',
    response_model=FilmList,
    summary='Главная страница',
    description='Популярные фильмы и фильтрация по жанрам',
    response_description='Название и рейтинг фильмов',
)
async def films() -> list[BaseFilm]:
    pass


@router.get(
    '/films/{film_id}',
    response_model=Film,
    summary='Страница фильма',
    description='Полная информация по фильму',
    response_description='Название, описание, рейтинг, жанры и персонал съемочной группы',
)
async def film_by_pk() -> Film:
    pass


@router.get(
    '/films/search',
    response_model=FilmList,
    summary='Поиск фильмов',
    description='Полнотекстовый поиск по названиям фильмов',
    response_description='Название и рейтинг фильмов',
)
async def search_films() -> list[BaseFilm]:
    pass
