from __future__ import annotations

import logging
import sqlite3
from os import environ
from typing import TYPE_CHECKING, Iterator

import psycopg2
from psycopg2._psycopg import connection as postgres_connection_object
from psycopg2.extras import DictCursor, execute_values

from schemas import (
    FilmworkPg,
    FilmworkSQLite,
    GenreFilmworkPg,
    GenreFilmworkSQLite,
    GenrePg,
    GenreSQLite,
    PersonFilmworkPg,
    PersonFilmworkSQLite,
    PersonPg,
    PersonSQLite,
    TableBatchDump,
)

if TYPE_CHECKING:
    from movies_types import PgSchema, PgSchemaClass, SQLiteSchemaClass
    SQL = str

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


def create_schema_if_not_exists(dsn: dict[str, str | int]) -> None:
    connection: postgres_connection_object = psycopg2.connect(**dsn)
    cursor = connection.cursor()
    cursor.execute('CREATE SCHEMA IF NOT EXISTS content;')
    connection.commit()
    cursor.close()
    connection.close()


class SQLiteDataExtraction:
    def __init__(self, sqlite_connection: sqlite3.Connection):
        self.sqlite_connection = sqlite_connection
        self.sqlite_connection.row_factory = sqlite3.Row

    @staticmethod
    def _get_paginated_results(
        cursor: sqlite3.Cursor,
        schema_class: SQLiteSchemaClass,
    ) -> Iterator[list[PgSchema]]:
        data = []
        while True:
            results = cursor.fetchmany(500)
            if not results:
                break
            for row in results:
                data.append(schema_class(**row).to_pg())
            yield data
            data = []

    def _load_table(
        self,
        sql: SQL,
        schema_class: SQLiteSchemaClass,
    ) -> Iterator[list[PgSchema]]:
        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError as e:
            logging.error(f'SQLite operational error: `{e}`')
            raise
        else:
            yield from self._get_paginated_results(cursor, schema_class)
        finally:
            cursor.close()

    def load_table(
        self,
        sql: SQL,
        schema_class: SQLiteSchemaClass,
    ) -> Iterator[list[PgSchema]]:
        yield from self._load_table(sql, schema_class)

    def load_batches(self) -> Iterator[TableBatchDump]:
        """Загружайте данные из sqlite частями размером 500."""
        schema_sql_map: dict[SQLiteSchemaClass, SQL] = {
            FilmworkSQLite: """SELECT * FROM film_work""",
            PersonSQLite: """SELECT * FROM person""",
            GenreSQLite: """SELECT * FROM genre""",
            GenreFilmworkSQLite: """SELECT * FROM genre_film_work""",
            PersonFilmworkSQLite: """SELECT * FROM person_film_work""",
        }
        for schema, sql in schema_sql_map.items():
            for batch in self.load_table(sql, schema):
                yield TableBatchDump(schema_class=schema, data=batch)


class PostgresDataLoader:
    def __init__(self, postgres_connection: postgres_connection_object):
        self.postgres_connection = postgres_connection

    @staticmethod
    def _get_column_names(columns: tuple[str]) -> str:
        column_names = ', '.join(columns)
        return column_names.rstrip()

    def _save_table(
        self,
        table_data: list[PgSchema],
        schema_class: PgSchemaClass,
    ) -> None:
        with self.postgres_connection.cursor() as cursor:
            data = [row.to_tuple() for row in table_data]
            sql = f"""
            INSERT INTO {schema_class.db_tablename()}
            ({self._get_column_names(schema_class.db_fieldnames())})
            VALUES %s
            ON CONFLICT (id) DO NOTHING
            """
            try:
                execute_values(cursor, sql, data, page_size=50)
            except psycopg2.OperationalError as e:
                logging.error(f'psycopg2 operational error: `{e}`')
                cursor.close()
                raise

    def save_table(
        self,
        table_data: list[PgSchema],
        schema_class: PgSchemaClass,
    ) -> None:
        self._save_table(table_data, schema_class)

    def save_batch(self, batch: TableBatchDump) -> None:
        sqlite_to_pg_schema_map: dict[SQLiteSchemaClass, PgSchemaClass] = {
            FilmworkSQLite: FilmworkPg,
            GenreFilmworkSQLite: GenreFilmworkPg,
            GenreSQLite: GenrePg,
            PersonFilmworkSQLite: PersonFilmworkPg,
            PersonSQLite: PersonPg,
        }
        pg_schema_class = sqlite_to_pg_schema_map[batch.schema_class]
        logging.debug(
            f'Сохраняем данные в postgres, таблица: '
            f'{pg_schema_class.db_tablename()}'
        )
        self.save_table(table_data=batch.data, schema_class=pg_schema_class)


def load_from_sqlite(
    sqlite_connection: sqlite3.Connection,
    postgres_connection: postgres_connection_object
):
    logging.info('Начата выгрузка данных из SQLite и загрузка в PostgreSQL')

    sqlite_data_extraction = SQLiteDataExtraction(sqlite_connection)
    postgres_data_loader = PostgresDataLoader(postgres_connection)

    for batch in sqlite_data_extraction.load_batches():
        postgres_data_loader.save_batch(batch)


if __name__ == '__main__':
    dsn: dict[str, str | int] = {
        'dbname': environ.get('MOVIES_DB_NAME'),
        'user': environ.get('MOVIES_DB_USER'),
        'password': environ.get('MOVIES_DB_PASSWORD'),
        'host': environ.get('MOVIES_DB_HOST'),
        'port': int(environ.get('MOVIES_DB_PORT')),
    }
    create_schema_if_not_exists(dsn=dsn)
    with sqlite3.connect('db.sqlite') as sqlite_connection, \
            psycopg2.connect(**dsn, cursor_factory=DictCursor) as postgres_connection:
        load_from_sqlite(
            sqlite_connection=sqlite_connection,
            postgres_connection=postgres_connection,
        )
