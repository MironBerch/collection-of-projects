import logging
from abc import ABC, abstractmethod
from typing import Any, Iterator, Type

import sqlalchemy
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search, query
from pandas import DataFrame, read_sql

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


class BaseEngine(ABC):
    """Абстрактный `Engine` для выполнения CRUD-операций."""

    engines: dict | None = None

    def __init__(self, db_type: str):
        self.db_type = db_type

    @classmethod
    def get_subclasses(cls) -> Iterator[Type]:
        """Вспомогательный метод для получения все наследников данного класса."""
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass

    @classmethod
    def get_engine(cls, db_type: str) -> 'BaseEngine':
        """Получение `Engine` базы данных."""
        if cls.engines is None:
            cls.engines = {}
            for engine_cls in cls.get_subclasses():
                engine = engine_cls()
                cls.engines[engine.db_type] = engine
        return cls.engines[db_type]

    @abstractmethod
    def create(self, dataframe: DataFrame, uri: str, resource: str) -> int:
        """Вставка данных."""

    @abstractmethod
    def read(self, uri: str, resource: str) -> DataFrame:
        """Чтение данных."""

    @abstractmethod
    def update(self, dataframe: DataFrame, uri: str, resource: str):
        """Обновление данных."""

    @abstractmethod
    def delete(self, dataframe: DataFrame, uri: str, resource: str):
        """Удаление данных."""


class ElasticEngine(BaseEngine):
    """ETL-сервис для выполнения CRUD-операций в Elasticsearch."""

    def __init__(self):
        super().__init__('elasticsearch')

    def create(self, dataframe: DataFrame, uri: str, resource: str) -> int:
        """Вставка данных в индекс."""
        def doc_generator(dataframe: DataFrame, index: str):
            for idx, document in dataframe.iterrows():
                yield {
                    '_index': index,
                    '_id': idx,
                    '_source': document.to_dict(),
                }
        try:
            with Elasticsearch(uri) as elastic:
                result = bulk(elastic, doc_generator(dataframe, resource), refresh=True)[0]
        except Exception as exception:
            logging.error(f'Create or update error: `{exception}`')
        return result

    def read(self, uri: str, resource: str) -> DataFrame:
        """Чтение данных из индекса."""
        try:
            with Elasticsearch(uri) as elastic:
                cursor = Search(using=elastic, index=resource)
                dataframe = DataFrame(doc.to_dict() for doc in cursor.scan())
        except Exception as exception:
            logging.error(f'Read error: `{exception}`')
        return dataframe

    def update(self, dataframe: DataFrame, uri: str, resource: str) -> int:
        """Обновление данных в индексе."""
        return self.create(dataframe, uri, resource)

    def delete(self, dataframe: DataFrame, uri: str, resource: str) -> int:
        """Удаление данных в индексе."""
        try:
            with Elasticsearch(uri) as elastic:
                ids = [index for index, _ in dataframe.iterrows()]
                docs = Search(using=elastic, index=resource).filter(query.Terms(_id=ids))
                result = docs.delete()['deleted']
        except Exception as exception:
            logging.error(f'Delete error: `{exception}`')
        return result


class SQLEngine(BaseEngine):
    """ETL-сервис для выполнения CRUD-операций в SQL базах данных."""

    def __init__(self):
        super().__init__('sql')

    def create(self, dataframe: DataFrame, uri: str, resource: str) -> int:
        """Вставка данных в таблицу."""
        try:
            with sqlalchemy.create_engine(uri).connect() as sql_conn:
                dataframe.to_sql(resource, sql_conn, if_exists='append', index=False)
                result = dataframe[dataframe.columns[0]].count()
        except Exception as exception:
            logging.error(f'Create error: `{exception}`')
        return result

    def read(self, uri: str, resource: str) -> DataFrame:
        """Чтение данных из таблицы."""
        try:
            with sqlalchemy.create_engine(uri).connect() as sql_conn:
                dataframe = read_sql(resource, sql_conn)
        except Exception as exception:
            logging.error(f'Read error: `{exception}`')
        return dataframe

    def update(self, dataframe: DataFrame, uri: str, resource: str) -> Any:
        """Обновление данных в таблице."""
        return NotImplemented

    def delete(self, dataframe: DataFrame, uri: str, resource: str) -> Any:
        """Удаление данных в таблице."""
        return NotImplemented


class SQLiteEngine(SQLEngine):
    """ETL-сервис для выполнения CRUD-операций в SQLite базах данных."""

    def __init__(self):
        super(SQLEngine, self).__init__('sqlite')


class PostgresEngine(SQLEngine):
    """ETL-сервис для выполнения CRUD-операций в PostgreSQL базах данных."""

    def __init__(self):
        super(SQLEngine, self).__init__('postgresql')
