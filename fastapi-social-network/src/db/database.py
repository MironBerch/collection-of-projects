import psycopg2
from psycopg2._psycopg import connection as connection_object, cursor
from psycopg2.extras import DictCursor


def create_connection() -> connection_object:
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='db',
        port='5432',
        cursor_factory=DictCursor,
    )


def create_cursor(connection: connection_object) -> cursor:
    return connection.cursor(cursor_factory=DictCursor)
