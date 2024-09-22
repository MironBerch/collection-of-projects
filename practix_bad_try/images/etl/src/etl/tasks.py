import pandas
from celery import shared_task

from etl.etl.operators import Join, Load, Select, Sync, Transform
from etl.models import Process


@shared_task(name='transfer_data')
def transfer_data(process_pk: int) -> str:
    """
    Функция для реализации одноразовой передачи данных.

    :arg process_pk: Первичный ключ процесса

    :return str: Результат передачи данных
    """
    process = Process.objects.get(pk=process_pk)
    dataframe = (
        pandas.DataFrame()
        .pipe(
            Select,
            process.source,
            process.from_table,
        )
        .pipe(
            Join,
            process.source,
            process.from_table,
            process.relationships.all(),
            process.index_column
        )
        .pipe(
            Transform,
            process.model,
            process.relationships.all()
        )
        .pipe(
            Load,
            process.target,
            process.to_table,
        )
    )
    return f'процесс={process}, загружено={dataframe.inserted_rows}'


@shared_task(name='sync_data')
def sync_data(process_pk: int) -> str:
    """
    Функция для реализации синхронизации данных между источником и целью.

    :arg process_pk: Первичный ключ процесса

    :return str: Результат передачи данных
    """
    process = Process.objects.get(pk=process_pk)
    dataframe = (
        pandas.DataFrame()
        .pipe(
            Select,
            process.target,
            process.to_table,
        )
        .pipe(
            Transform,
            process.model,
            process.relationships.all(),
        )
        .pipe(
            Sync,
            process.target,
            process.to_table,
            process.index_column,
            source_dataframe=(
                pandas.DataFrame()
                .pipe(
                    Select,
                    process.source,
                    process.from_table,
                )
                .pipe(
                    Join,
                    process.source,
                    process.from_table,
                    process.relationships.all(),
                    process.index_column
                )
                .pipe(
                    Transform,
                    process.model,
                    process.relationships.all(),
                )
            )
        )
    )
    result = (
        f'процесс={process}',
        f'загружено={dataframe.inserted_rows}',
        f'обновлено={dataframe.updated_rows}',
        f'удалено={dataframe.deleted_rows}',
    )
    return ', '.join(result)
