from typing import Tuple

from pandas import DataFrame, merge

from etl_panel.models import Relationship


class Aggregation:
    """ETL-сервис агрегации данных датафреймов."""

    @staticmethod
    def get_column(
        dataframes: dict[str, DataFrame],
        relation: Relationship,
        index_column: str,
        table: str,
    ) -> DataFrame:
        """
        Объединения связанных таблиц по определенным параметрам
        и получения новой колонки из полученных данных.
        """
        return (
            merge(
                left=dataframes[relation.through_table].drop(index_column, axis='columns'),
                right=dataframes[relation.table],
                how='left',
                left_on=relation.table + relation.suffix,
                right_on=index_column,
            )
            .query(relation.condition if relation.condition is not None else 'index == index')
            .groupby(by=table + relation.suffix)[[col.name for col in relation.model.columns.all()]]
            .apply(
                func=lambda row: list(row.to_numpy().flat)
                if relation.flat else row.to_dict('records'),
            )
            .to_frame(relation.related_name)
        )

    @staticmethod
    def get_data_changes(
        source: DataFrame,
        destination: DataFrame,
        index_column: str,
    ) -> Tuple[DataFrame, ...]:
        """Функция для сравения датафреймов таблиц источника и получателя данных."""
        destination.set_index(index_column, inplace=True, drop=False)
        changes = source[
            ~source.apply(tuple, axis='columns').isin(destination.apply(tuple, axis='columns'))
        ]
        deleted = destination[
            ~destination.apply(tuple, axis='columns').isin(source.apply(tuple, axis='columns'))
        ].drop(changes.index.values, errors='ignore')
        if not changes.empty:
            new = changes[~changes[index_column].isin(destination[index_column])]
            modified = changes[changes[index_column].isin(destination[index_column])]
        else:
            new, modified = changes, changes
        return new, modified, deleted
