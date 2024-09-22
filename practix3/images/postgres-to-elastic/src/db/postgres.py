from contextlib import contextmanager
from os import environ
from typing import Iterator

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor


@contextmanager
def get_postgres() -> Iterator[connection]:
    """
    Функция с контекстным менеджером для подключении к базе данных PostgreSQL.
    """
    dsn: dict[str, str | int] = {
        'dbname': environ.get('MOVIES_DB_NAME'),
        'user': environ.get('MOVIES_DB_USER'),
        'password': environ.get('MOVIES_DB_PASSWORD'),
        'host': environ.get('MOVIES_DB_HOST'),
        'port': int(environ.get('MOVIES_DB_PORT')),
        'options': '-c search_path=content',
    }
    conn: connection = psycopg2.connect(**dsn)
    conn.cursor_factory = DictCursor
    yield conn
    conn.close()
