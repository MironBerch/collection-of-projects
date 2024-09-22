from dataclasses import dataclass
from typing import Any, Iterator

from redis import Redis
from redis.exceptions import ConnectionError

from core.constants import BATCH_SIZE
from core.decorators import backoff
from core.types import PostgresRow, Schemas
from models.movie import Movie
from models.person import Person


@dataclass
class DataTransform(object):
    """Класс для преобразования данных и хранения в Redis промежуточных результатов."""

    redis: Redis

    @backoff(exceptions=(ConnectionError, ))
    def collector(self, key: str, film_work_id: str) -> None:
        """Собирает id фильмов, которые нужно обновить в данный момент.

        - хранит в хранилище Redis
        - тип данных - множество (SET)
        """
        self.redis.sadd(key, film_work_id)

    @backoff(exceptions=(ConnectionError, ))
    def batcher(self, key: str) -> Iterator[dict[str, Schemas]]:
        """Итерирует данные из Redis по пачкам и генерирует словари.

        - делит данные с id фильмов и декодирует их из байтов в строки
        - генерирует словари, где ключи - id фильмов, а значения - схема модели фильма
        - после окончании итераций, удаляет id фильмов, которые нужно обновить в данный момент
        """
        cursor = '0'
        while cursor != 0:
            cursor, data = self.redis.sscan(key, cursor=cursor, count=BATCH_SIZE)
            yield {movie_id.decode(): Movie.properties() for movie_id in data}
        self.redis.delete(key)

    def parser(self, row: PostgresRow, movie: dict) -> None:
        """Парсирует данные формата PostgreSQL и добавляет их к соответствующему фильму."""
        if not movie['id']:
            movie['id'] = row['id']
            movie['title'] = row['title']
            movie['description'] = row['description']
            movie['rating'] = row['rating']
        movie.update(self.add_person(row, movie) if row['person_id'] else {})
        movie.update(self.add_genre(row, movie) if row['genre_name'] else {})

    def add_person(self, row: PostgresRow, movie: dict) -> dict:
        """Добавляет и распределяет данные с участниками фильма по ролям."""
        role = f'{row["role"]}s'
        role_names = f'{row["role"]}s_names'
        persons_list: list = movie.get(role, [])
        person_names_list: list = movie.get(role_names, [])
        person = Person(id=row['person_id'], full_name=row['full_name'])
        if person not in persons_list:
            persons_list.append(person)
            person_names_list.append(person.full_name)
        return {role: persons_list, role_names: person_names_list}

    def add_genre(self, row: PostgresRow, movie: dict) -> dict:
        """Добавляет данные с жанрами к фильму."""
        genre_names_list: list = movie.get('genre', [])
        if row['genre_name'] not in genre_names_list:
            genre_names_list.append(row['genre_name'])
        return {'genre': genre_names_list}
