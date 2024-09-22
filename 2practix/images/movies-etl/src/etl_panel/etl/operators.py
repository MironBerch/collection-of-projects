from pandas import DataFrame

from django.db.models.query import QuerySet

from etl_panel.etl.aggregation import Aggregation
from etl_panel.etl.engines import BaseEngine
from etl_panel.etl.validation import Validation
from etl_panel.models import Database, Model, Relationship


class Select(DataFrame):
    """ETL-оператор для извлечения данных из таблицы базы данных."""

    def __init__(self, dataframe: DataFrame, db: Database, table: str):
        """При инициализации ожидает получить данные об источнике."""
        engine = BaseEngine.get_engine(db.type)
        dataframe = engine.read(db.uri, table)
        super().__init__(data=dataframe)


class Join(DataFrame):
    """ETL-оператор для объединения таблиц по определённым параметрам и получния нужных данных."""

    def __init__(
            self,
            dataframe: DataFrame,
            db: Database,
            table: str,
            relations: QuerySet[Relationship],
            index_column: str,
    ):
        """
        При инициализации ожидает получить данные об источнике вместе с присоединёнными таблицами.
        """
        if not dataframe.empty:
            engine = BaseEngine.get_engine(db.type)
            dataframes = {
                table: engine.read(
                    db.uri,
                    table,
                ) for rel in relations for table in (
                    rel.table,
                    rel.through_table,
                )
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


class Transform(DataFrame):
    """ETL-оператор для валидации и трансформации данных."""

    def __init__(self, dataframe: DataFrame, model: Model, relations: QuerySet[Relationship]):
        """
        При инициализации ожидает получить данные модели
        передачи данных вместе с вложенными объектах.
        """
        if not dataframe.empty:
            schema = Validation.get_schema(model, relations)
            dataframe = dataframe.apply(schema.validate_row, axis='columns')
        super().__init__(data=dataframe)


class Load(DataFrame):
    """ETL-оператор для загрузки данных их получателю."""

    def __init__(self, dataframe: DataFrame, db: Database, table: str):
        """При инициализации ожидает получить данные о получателе."""
        inserted_rows = 0
        if not dataframe.empty:
            engine = BaseEngine.get_engine(db.type)
            inserted_rows = engine.create(dataframe, db.uri, table)
        super().__init__(data=dataframe)
        self.inserted_rows = inserted_rows


class Sync(DataFrame):
    """ETL-оператор для синхронизации данных между источником и получателем."""

    def __init__(
            self,
            dataframe: DataFrame,
            db: Database,
            table: str,
            index_column: str,
            source_dataframe: DataFrame,
    ):
        """При инициализации ожидает получить данные об источнике и получателе."""
        engine = BaseEngine.get_engine(db.type)
        inserted_rows, updated_rows, deleted_rows = 0, 0, 0
        if not dataframe.empty:
            new, modified, deleted = Aggregation.get_data_changes(
                source_dataframe,
                dataframe,
                index_column,
            )
            inserted_rows = engine.create(new, db.uri, table) if not new.empty else 0
            updated_rows = engine.update(modified, db.uri, table) if not modified.empty else 0
            deleted_rows = engine.delete(deleted, db.uri, table) if not deleted.empty else 0
        else:
            inserted_rows = engine.create(
                source_dataframe,
                db.uri,
                table,
            ) if not source_dataframe.empty else 0
        super().__init__(data=dataframe)
        self.inserted_rows = inserted_rows
        self.updated_rows = updated_rows
        self.deleted_rows = deleted_rows
