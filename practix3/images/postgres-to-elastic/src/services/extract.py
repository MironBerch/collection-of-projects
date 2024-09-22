from datetime import datetime
from typing import Iterator

from psycopg2 import InterfaceError, OperationalError
from psycopg2.extensions import connection, cursor
from psycopg2.extras import DictRow
from pydantic.dataclasses import dataclass

from core.constants import BATCH_SIZE
from core.decorators import backoff
from services.base import Config, UpdatesNotFoundError


@dataclass(config=Config)
class PostgresExtractor(object):
    """Класс для получения данных из PostgreSQL."""

    postgres: connection

    TABLES = ('film_work', 'person', 'genre')

    @backoff(exceptions=(InterfaceError, OperationalError))
    def select_table(self, table: str, timestamp: datetime) -> cursor:
        """Запрашивает обновления в таблице на текущий момент."""
        curs = self.postgres.cursor()
        query = """
            SELECT *
            FROM {table}
            WHERE modified > TIMESTAMP '{timestamp}'
            ORDER BY modified;
        """
        curs.execute(query.format(table=table, timestamp=timestamp))
        return curs

    @backoff(exceptions=(InterfaceError, OperationalError))
    def get_updates(self, timestamp: datetime) -> Iterator[tuple[str, list]]:
        """Извлекает новые данные с момента последнего обновления."""
        updates = {table: self.select_table(table, timestamp) for table in self.TABLES}
        if not any(curs.rowcount for curs in updates.values()):
            raise UpdatesNotFoundError
        for table, curs in updates.items():
            while data := curs.fetchmany(BATCH_SIZE):
                yield (table, data)
            curs.close()

    @backoff(exceptions=(InterfaceError, OperationalError))
    def get_film_work_ids(self, table: str, data: list[DictRow]) -> Iterator[DictRow]:
        """Извлекает id фильмов, в которых произошли изменения."""
        if table in {'person', 'genre'}:
            with self.postgres.cursor() as curs:
                film_ids = [f"'{row['id']}'" for row in data]
                query = """
                    SELECT film_work.id
                    FROM film_work
                    LEFT JOIN {table}_film_work gp_film_work \
                        ON gp_film_work.film_work_id = film_work.id
                    WHERE gp_film_work.{table}_id IN ({film_ids})
                    ORDER BY film_work.modified;
                """
                curs.execute(query.format(table=table, film_ids=', '.join(film_ids)))
                yield from curs
        else:
            yield from data

    @backoff(exceptions=(InterfaceError, OperationalError))
    def get_movie_data(self, film_ids: list[str]) -> Iterator[DictRow]:
        """Извлекает информацию для записи в индекс Elasticsearch с названием `movies`."""
        with self.postgres.cursor() as curs:
            film_ids = [f"'{film_id}'" for film_id in film_ids]
            query = """
                SELECT
                    film_work.id,
                    film_work.title,
                    film_work.description,
                    film_work.rating,
                    person_film_work.role,
                    person.id as person_id,
                    person.full_name,
                    genre.name as genre_name
                FROM film_work
                LEFT JOIN person_film_work ON person_film_work.film_work_id = film_work.id
                LEFT JOIN person ON person.id = person_film_work.person_id
                LEFT JOIN genre_film_work ON genre_film_work.film_work_id = film_work.id
                LEFT JOIN genre ON genre.id = genre_film_work.genre_id
                WHERE film_work.id IN ({film_ids})
            """
            curs.execute(query.format(film_ids=', '.join(film_ids)))
            yield from curs
