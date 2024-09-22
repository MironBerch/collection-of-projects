from typing import Type

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
)

PgSchema = FilmworkPg | GenreFilmworkPg | GenrePg | PersonFilmworkPg | PersonPg
PgSchemaClass = Type[FilmworkPg] | \
    Type[GenreFilmworkPg] | \
    Type[GenrePg] | \
    Type[PersonFilmworkPg] | \
    Type[PersonPg]
SQLiteSchemaClass = Type[FilmworkSQLite] | \
        Type[GenreFilmworkSQLite] | \
        Type[GenreSQLite] | \
        Type[PersonFilmworkSQLite] | \
        Type[PersonSQLite]
