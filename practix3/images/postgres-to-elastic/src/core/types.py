from typing import Type

from psycopg2.extras import DictRow

from models.genre import Genre
from models.movie import Movie
from models.person import Person

PostgresRow = DictRow

Schemas = Type[Genre] | Type[Person] | Type[Movie]
