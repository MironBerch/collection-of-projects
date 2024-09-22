from datetime import datetime
from time import sleep

from elasticsearch import Elasticsearch
from psycopg2.extensions import connection
from pytz import timezone
from redis import Redis

from core.logger import logger
from db.elastic import get_elastic
from db.postgres import get_postgres
from db.redis import get_redis
from models.genre import Genre
from models.movie import Movie
from models.person import Person
from services.base import UpdatesNotFoundError
from services.extract import PostgresExtractor
from services.load import ElasticsearchLoader
from services.state import RedisStorage, State
from services.transform import DataTransform


def etl_process(
    postgres: PostgresExtractor,
    data: DataTransform,
    elastic: ElasticsearchLoader,
    state: State,
) -> None:
    """Запускает внутренние компоненты процесса Extract-Transform-Load."""
    timestamp = state.read_state('last_updated', datetime.min)
    for table, rows in postgres.get_updates(timestamp):
        if table == 'person':
            elastic.bulk_insert(Person, rows)
        if table == 'genre':
            elastic.bulk_insert(Genre, rows)
        for row in postgres.get_film_work_ids(table, rows):
            data.collector('movie_ids', row['id'])
    for movies in data.batcher('movie_ids'):
        for row in postgres.get_movie_data(movies.keys()):
            data.parser(row, movies.get(row['id']))
        elastic.bulk_insert(Movie, movies.values())


def postgres_to_elastic(
        postgres: connection,
        elastic: Elasticsearch,
        redis: Redis,
) -> None:
    """Основной метод загрузки данных из PostgreSQL в Elasticsearch."""
    state = State(RedisStorage(redis))
    while True:
        try:
            etl_process(
                PostgresExtractor(postgres),
                DataTransform(redis),
                ElasticsearchLoader(elastic),
                state,
            )
        except UpdatesNotFoundError:
            logger.info('Нет обновлений.')
        else:
            logger.info('Есть обновления!')
            state.write_state('last_updated', datetime.now(tz=timezone('Europe/Moscow')))
        finally:
            logger.info('Повторный запрос через 1 минуту.')
            sleep(60)


if __name__ == '__main__':
    with get_postgres() as postgres_connection:
        with get_elastic() as elastic_connection:
            with get_redis() as redis_connection:
                postgres_to_elastic(
                    postgres=postgres_connection,
                    elastic=elastic_connection,
                    redis=redis_connection,
                )
