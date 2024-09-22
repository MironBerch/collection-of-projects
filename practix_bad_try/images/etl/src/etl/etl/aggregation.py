import pandas as pd

from etl.models import Relationship


class Aggregation:
    """ETL-сервис агрегации данных датафреймов."""

    @staticmethod
    def get_column(
        dataframes: dict[str, pd.DataFrame],
        relation: Relationship,
        index_column: str,
        table: str,
    ) -> pd.DataFrame:
        """
        Объединения связанных таблиц по определенным параметрам
        и получения новой колонки из полученных данных.

        :arg dataframes: Датафреймы связанных таблицы
        :arg relation: Метаинформация о связях таблиц
        :arg index_column: Название колонки для индексации данных
        :arg table: Название родительской таблицы для группировки по ней

        :return pd.DataFrame: Датафрейм, состоящий из полученной колонки
        """

        return (
            pd.merge(
                left=dataframes[relation.through_table].drop(index_column, axis='columns'),
                right=dataframes[relation.table],
                how='left',
                left_on=relation.table + relation.suffix,
                right_on=index_column,
            )
            .query(
                relation.condition if relation.condition is not None else 'index == index'
            )
            .groupby(
                by=table + relation.suffix,
            )[[col.name for col in relation.model.columns.all()]]
            .apply(
                func=lambda row: list(
                    row.to_numpy().flat,
                ) if relation.flat else row.to_dict('records')
            )
            .to_frame(relation.related_name)
        )

    @staticmethod
    def get_data_changes(
        src: pd.DataFrame,
        dest: pd.DataFrame,
        index_column: str,
    ) -> tuple[pd.DataFrame, ...]:
        """
        Функция для сравения датафреймов таблиц источника и получателя данных.

        :arg src: Датафрейм источника
        :arg dest: Датафрейм получателя
        :arg index_column: Название колонки для индексации данных

        :return tuple[pd.DataFrame, ...]: Датафреймы с новыми, обновленными и удаленными данными
        """

        dest.set_index(index_column, inplace=True, drop=False)
        changes = src[~src.apply(tuple, axis='columns').isin(dest.apply(tuple, axis='columns'))]
        deleted = dest[
            ~dest.apply(tuple, axis='columns').isin(src.apply(tuple, axis='columns'))
        ].drop(changes.index.values, errors='ignore')
        if not changes.empty:
            new = changes[~changes[index_column].isin(dest[index_column])]
            modified = changes[changes[index_column].isin(dest[index_column])]
        else:
            new, modified = changes, changes
        return new, modified, deleted
