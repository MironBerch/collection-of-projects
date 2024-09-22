from fastapi import APIRouter

from models.genre import Genre, GenreList

router = APIRouter(tags=['genres'])


@router.get(
    '/genres',
    response_model=GenreList,
    summary='Жанры',
    description='Список жанров',
    response_description='Название и описание жанров',
)
async def genres() -> list[Genre]:
    pass


@router.get(
    '/genres/{genre_id}',
    response_model=Genre,
    summary='Страница жанра',
    description='Полная информация по жанру',
    response_description='Название и описание жанра',
)
async def genre_by_pk() -> Genre:
    pass
