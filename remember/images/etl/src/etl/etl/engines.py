from abc import ABC, abstractmethod
from typing import Iterator, Type

import pandas as pd
import sqlalchemy
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import bulk
from elasticsearch.helpers.errors import BulkIndexError
from elasticsearch_dsl import Search, query
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

from etl.etl.errors import (
    ExtractConnectionError,
    ExtractTableError,
    LoadConnectionError,
    LoadTableError,
)


class CRUD(ABC):
    """Абстрактный ETL-сервис для выполнения CRUD-операций."""

    engines: dict | None = None

    def __init__(self, db_type: str):
        """
        При инициализации ожидает получить тип базы данных.

        :arg db_type: Тип базы данных
        """

        self.db_type = db_type

    @classmethod
    def get_subclasses(cls) -> Iterator[Type]:
        """
        Вспомогательный метод для получения все наследников данного класса.

        :yields Iterator[type]:  Наследники класса
        """

        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass

    @classmethod
    def get_engine(cls, db_type: str) -> 'CRUD':
        """
        Получение движка базы данных для реализации CRUD сервиса.

        :arg db_type: Тип БД

        :return CRUD: Объект CRUD сервиса
        """

        if cls.engines is None:
            cls.engines = {}
            for engine_cls in cls.get_subclasses():
                engine = engine_cls()
                cls.engines[engine.db_type] = engine
        return cls.engines[db_type]

    @abstractmethod
    def create(self, dataframe: pd.DataFrame, uri: str, resource: str) -> int:
        """
        Вставка данных.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста БД
        :arg resource: Название ресурса, куда вставляем данные

        :return int: Количество вставленных документов
        """

    @abstractmethod
    def read(self, uri: str, resource: str) -> pd.DataFrame:
        """
        Чтение данных.

        :arg uri: Имя хоста БД
        :arg resource: Название ресурса, от куда извлекаем данные

        :return pd.DataFrame: Датафрейм таблицы
        """

    @abstractmethod
    def update(self, dataframe: pd.DataFrame, uri: str, resource: str):
        """
        Обновление данных.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста БД
        :arg resource: Название ресурса, где изменяем данные

        :return int: Количество обновленных документов
        """

    @abstractmethod
    def delete(self, dataframe: pd.DataFrame, uri: str, resource: str):
        """
        Удаление данных.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста БД
        :arg resource: Название ресурса, от куда удаляем данные

        :retur int: Количество удалённых документов
        """


class ElasticEngine(CRUD):
    """ETL-сервис для выполнения CRUD-операций в Elasticsearch."""

    def __init__(self):
        super().__init__('elasticsearch')

    def create(self, dataframe: pd.DataFrame, uri: str, resource: str) -> int:
        """
        Вставка данных в индекс.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста
        :arg resource: Название индекса

        :raise LoadTableError: Ошибка индекса
        :raise LoadConnectionError: Ошибка подключения

        :return int: Количество вставленных документов
        """

        def doc_generator(dataframe: pd.DataFrame, index: str):
            for idx, document in dataframe.iterrows():
                yield {
                    '_index': index,
                    '_id': idx,
                    '_source': document.to_dict(),
                }
        try:
            with Elasticsearch(uri) as elastic:
                result = bulk(elastic, doc_generator(dataframe, resource), refresh=True)[0]
        except BulkIndexError as exc:
            raise LoadTableError(str(exc.errors[0]))
        except ConnectionError as exc:
            raise LoadConnectionError(exc.error)
        return result

    def read(self, uri: str, resource: str) -> pd.DataFrame:
        """
        Чтение данных из индекса.

        :arg uri: Имя хоста
        :arg resource: Название индекса

        :raise ExtractTableError: Ошибка индекса
        :raise ExtractConnectionError: Ошибка подключения

        :return pd.DataFrame: Датафрейм индекса
        """

        try:
            with Elasticsearch(uri) as elastic:
                cursor = Search(using=elastic, index=resource)
                dataframe = pd.DataFrame(doc.to_dict() for doc in cursor.scan())
        except NotFoundError as exc:
            raise ExtractTableError(exc.error)
        except ConnectionError as exc:
            raise ExtractConnectionError(exc.error)
        return dataframe

    def update(self, dataframe: pd.DataFrame, uri: str, resource: str) -> int:
        """
        Обновление данных в индексе.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста
        :arg resource: Название индекса

        :return int: Количество обновленных документов
        """

        return self.create(dataframe, uri, resource)

    def delete(self, dataframe: pd.DataFrame, uri: str, resource: str):
        """
        Удаление данных в индексе.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста
        :arg resource: Название индекса

        :raise LoadTableError: Ошибка индекса
        :raise LoadConnectionError: Ошибка подключения

        :return int: Количество удалённых документов
        """

        try:
            with Elasticsearch(uri) as elastic:
                ids = [index for index, _ in dataframe.iterrows()]
                docs = Search(using=elastic, index=resource).filter(query.Terms(_id=ids))
                result = docs.delete()['deleted']
        except NotFoundError as exc:
            raise LoadTableError(exc.error)
        except ConnectionError as exc:
            raise LoadConnectionError(exc.error)
        return result


class SQLEngine(CRUD):
    """ETL-сервис для выполнения CRUD-операций в SQL базах данных."""

    def __init__(self):
        super().__init__('sql')

    def create(self, dataframe: pd.DataFrame, uri: str, resource: str):
        """
        Вставка данных в таблицу.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста
        :arg resource: Название индекса

        :raise LoadTableError: Ошибка таблицы
        :raise LoadConnectionError: Ошибка подключения

        :return int: Количество вставленных строк
        """

        try:
            with sqlalchemy.create_engine(uri).connect() as sql_connection:
                dataframe.to_sql(resource, sql_connection, if_exists='append', index=False)
                result = dataframe[dataframe.columns[0]].count()
        except (OperationalError, ProgrammingError, IntegrityError) as exc:
            if exc.statement:
                raise LoadTableError(detail=str(exc.orig))
            else:
                raise LoadConnectionError(detail=str(exc.orig))
        return result

    def read(self, uri: str, resource: str) -> pd.DataFrame:
        """
        Чтение данных из таблицы.

        :arg uri: Имя хоста
        :arg resource: Название таблицы

        :raise ExtractTableError: Ошибка таблицы
        :raise ExtractConnectionError: Ошибка подключения

        :return pd.DataFrame: Датафрейм таблицы
        """

        try:
            with sqlalchemy.create_engine(uri).connect() as sql_connection:
                dataframe = pd.read_sql(resource, sql_connection)
        except (OperationalError, ProgrammingError) as exc:
            if exc.statement == resource:
                raise ExtractTableError(detail=str(exc.orig))
            else:
                raise ExtractConnectionError(detail=str(exc.orig))
        return dataframe

    def update(self, dataframe: pd.DataFrame, uri: str, resource: str) -> int:
        """
        Обновление данных в таблице.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста
        :arg resource: Название таблицы

        :return int: Количество обновленных документов
        """

        try:
            with sqlalchemy.create_engine(uri).connect() as sql_connection:
                for _, row in dataframe.iterrows():
                    sql = f"UPDATE {resource} SET "
                    updates = ', '.join([f"{column} = '{value}'" for column, value in row.items()])
                    sql += updates
                    sql_connection.execute(sql)
        except (OperationalError, ProgrammingError, IntegrityError) as exc:
            if exc.statement:
                raise LoadTableError(detail=str(exc.orig))
            else:
                raise LoadConnectionError(detail=str(exc.orig))
        return len(dataframe)

    def delete(self, dataframe: pd.DataFrame, uri: str, resource: str) -> int:
        """
        Удаление данных в таблице.

        :arg dataframe: Датафрейм
        :arg uri: Имя хоста
        :arg resource: Название таблицы

        :return int: Количество удалённых документов
        """

        try:
            with sqlalchemy.create_engine(uri).connect() as sql_connection:
                for index in dataframe.index:
                    sql = f"DELETE FROM {resource} WHERE id = '{index}'"
                    sql_connection.execute(sql)
        except (OperationalError, ProgrammingError, IntegrityError) as exc:
            if exc.statement:
                raise LoadTableError(detail=str(exc.orig))
            else:
                raise LoadConnectionError(detail=str(exc.orig))
        return len(dataframe)


class SQLiteEngine(SQLEngine):
    """ETL-сервис для выполнения CRUD-операций в SQLite базах данных."""

    def __init__(self):
        super(SQLEngine, self).__init__('sqlite')


class PostgresEngine(SQLEngine):
    """ETL-сервис для выполнения CRUD-операций в PostgreSQL базах данных."""

    def __init__(self):
        super(SQLEngine, self).__init__('postgresql')
