import pandas as pd

from django.db.models.query import QuerySet

from etl.etl.aggregation import Aggregation
from etl.etl.engines import CRUD
from etl.etl.validation import Validation
from etl.models import Database, Model, Relationship


class Select(pd.DataFrame):
    """ETL-оператор для извлечения данных из таблицы базы данных."""

    def __init__(self, dataframe: pd.DataFrame, database: Database, table: str):
        """
        При инициализации ожидает получить данные об источнике.

        :arg dataframe: Датафрейм
        :arg database: Данные БД
        :arg table: Название таблицы
        """

        engine = CRUD.get_engine(database.type)
        dataframe = engine.read(database.uri, table)
        super().__init__(data=dataframe)


class Join(pd.DataFrame):
    """ETL-оператор для объединения таблиц по определённым параметрам и получния нужных данных."""

    def __init__(
            self,
            dataframe: pd.DataFrame,
            database: Database,
            table: str,
            relations: QuerySet[Relationship],
            index_column: str,
    ):
        """
        При инициализации ожидает получить данные об источнике вместе с присоединёнными таблицами.

        :arg dataframe: Датафрейм
        :arg database: Данные БД
        :arg table: Название таблицы
        :arg relations: Связи с другими таблицами
        :arg index_column: Колонка для индексации данных
        """

        if not dataframe.empty:
            engine = CRUD.get_engine(database.type)
            dataframes = {
                table: engine.read(
                    database.uri,
                    table,
                ) for rel in relations for table in (rel.table, rel.through_table)
            }
            new_columns = [
                Aggregation.get_column(
                    dataframes,
                    rel,
                    index_column,
                    table,
                ) for rel in relations
            ]
            dataframe = dataframe.set_index(index_column, drop=False).join(new_columns)
        super().__init__(data=dataframe)


class Transform(pd.DataFrame):
    """ETL-оператор для валидации и трансформации данных."""

    def __init__(self, dataframe: pd.DataFrame, model: Model, relations: QuerySet[Relationship]):
        """
        При инициализации ожидает данные модели передачи данных вместе с вложенными объектах.

        :arg dataframe: Датафрейм
        :arg model: Модель данных
        :arg relations: Данные по связанным таблицам
        """

        if not dataframe.empty:
            schema = Validation.get_schema(model, relations)
            dataframe = dataframe.apply(schema.validate_row, axis='columns')
        super().__init__(data=dataframe)


class Load(pd.DataFrame):
    """ETL-оператор для загрузки данных их получателю."""

    def __init__(self, dataframe: pd.DataFrame, database: Database, table: str):
        """
        При инициализации ожидает получить данные о получателе.

        :arg dataframe: Датафрейм
        :arg database: Данные БД
        :arg table: Название таблицы
        """

        inserted_rows = 0
        if not dataframe.empty:
            engine = CRUD.get_engine(database.type)
            inserted_rows = engine.create(dataframe, database.uri, table)
        super().__init__(data=dataframe)
        self.inserted_rows = inserted_rows


class Sync(pd.DataFrame):
    """ETL-оператор для синхронизации данных между источником и получателем."""

    def __init__(
            self,
            dataframe: pd.DataFrame,
            database: Database,
            table: str,
            index_column: str,
            source_dataframe: pd.DataFrame,
    ):
        """
        При инициализации ожидает получить данные об источнике и получателе.

        :arg dataframe: Датафрейм получателя
        :arg database: Данные БД
        :arg table: Название таблицы
        :arg index_column: Колонка для индексации данных
        :arg source_dataframe: Датафрейм источника
        """

        engine = CRUD.get_engine(database.type)
        inserted_rows, updated_rows, deleted_rows = 0, 0, 0
        if not dataframe.empty:
            new, modified, deleted = Aggregation.get_data_changes(
                source_dataframe,
                dataframe,
                index_column,
            )
            inserted_rows = engine.create(
                new,
                database.uri,
                table,
            ) if not new.empty else 0
            updated_rows = engine.update(
                modified,
                database.uri,
                table,
            ) if not modified.empty else 0
            deleted_rows = engine.delete(
                deleted,
                database.uri,
                table,
            ) if not deleted.empty else 0
        else:
            inserted_rows = engine.create(
                source_dataframe,
                database.uri,
                table,
            ) if not source_dataframe.empty else 0
        super().__init__(data=dataframe)
        self.inserted_rows = inserted_rows
        self.updated_rows = updated_rows
        self.deleted_rows = deleted_rows
