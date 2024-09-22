from celery import shared_task
from pandas import DataFrame

from etl_panel.etl.operators import Join, Load, Select, Sync, Transform
from etl_panel.models import Process


@shared_task(name='transfer_data')
def transfer_data(process_id: int) -> str:
    """Функция для реализации одноразовой передачи данных."""
    process = Process.objects.get(id=process_id)
    dataframe = (
        DataFrame()
        .pipe(Select, process.source, process.from_table)
        .pipe(
            Join,
            process.source,
            process.from_table,
            process.relationships.all(),
            process.index_column,
        )
        .pipe(Transform, process.model, process.relationships.all())
        .pipe(Load, process.target, process.to_table)
    )
    return f'процесс={process}, загружено={dataframe.inserted_rows}'


@shared_task(name='sync_data')
def sync_data(process_id: int) -> str:
    """Функция для реализации синхронизации данных между источником и целью."""
    process = Process.objects.get(id=process_id)
    dataframe = (
        DataFrame()
        .pipe(Select, process.target, process.to_table)
        .pipe(Transform, process.model, process.relationships.all())
        .pipe(
            Sync,
            process.target,
            process.to_table,
            process.index_column,
            source_df=(
                DataFrame()
                .pipe(Select, process.source, process.from_table)
                .pipe(
                    Join,
                    process.source,
                    process.from_table,
                    process.relationships.all(),
                    process.index_column,
                )
                .pipe(Transform, process.model, process.relationships.all())
            ),
        )
    )
    return 'процесс={}, загружено={}, обновлено={}, удалено={}'.format(
        process,
        dataframe.inserted_rows,
        dataframe.updated_rows,
        dataframe.deleted_rows,
    )
