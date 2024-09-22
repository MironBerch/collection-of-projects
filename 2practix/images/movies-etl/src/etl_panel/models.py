import json

from django.db import models
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from etl_panel.enums import DatabaseType, DataType, ProcessStatus, TimeInterval


class Database(models.Model):
    """Модель базы данных."""

    slug = models.SlugField(
        unique=True,
    )
    type = models.CharField(
        choices=DatabaseType.choices,
        max_length=50,
    )
    uri = models.CharField(
        max_length=255,
    )

    def __str__(self) -> str:
        return self.slug


class Model(models.Model):
    """Модель для схемы данных."""

    title = models.CharField(
        unique=True,
        max_length=255,
    )

    def __str__(self) -> str:
        return self.title


class Column(models.Model):
    """Модель для колонок схемы данных."""

    name = models.CharField(
        max_length=255,
    )
    type = models.CharField(
        choices=DataType.choices,
        max_length=50,
    )
    default = models.CharField(
        blank=True,
        max_length=255,
    )
    alias = models.CharField(
        blank=True,
        max_length=255,
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name='columns',
    )

    def __str__(self) -> str:
        prefix = f' DEFAULT {self.default}' if self.default is not None else ''
        return f'{self.alias or self.name}: {self.type.upper()}{prefix}'


class Process(models.Model):
    """Модель для процесса передачи данных."""

    slug = models.SlugField(
        unique=True,
    )
    source = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
        related_name='targets',
    )
    target = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
        related_name='sources',
    )
    status = models.CharField(
        choices=ProcessStatus.choices,
        default=ProcessStatus.ACTIVE,
        max_length=50,
    )
    from_table = models.CharField(
        max_length=255,
    )
    to_table = models.CharField(
        max_length=255,
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
    )
    index_column = models.CharField(
        max_length=255,
        default='id',
    )
    sync = models.BooleanField(
        default=False,
    )
    time_interval = models.CharField(
        choices=TimeInterval.choices,
        default=TimeInterval.ONE_MINUTE,
        max_length=50,
    )
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Processes'

    def __str__(self) -> str:
        return self.slug

    def delete(self, *args, **kwargs) -> tuple:
        """Удаление задачи вместе с процессом."""
        if self.task is not None:
            self.task.delete()
        return super().delete(*args, **kwargs)

    def setup_task(self):
        """Создание задачи в Celery."""
        self.task = PeriodicTask.objects.create(
            name=self.slug,
            task='sync_data' if self.sync else 'transfer_data',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now(),
            one_off=True if not self.sync else False,
        )
        self.save()

    @property
    def interval_schedule(self) -> IntervalSchedule:
        """Свойство для получения интервала времени."""
        if self.time_interval == TimeInterval.ONE_MINUTE:
            return IntervalSchedule.objects.get_or_create(
                every=1,
                period='minutes',
            )[0]
        if self.time_interval == TimeInterval.FIVE_MINUTES:
            return IntervalSchedule.objects.get_or_create(
                every=5,
                period='minutes',
            )[0]
        if self.time_interval == TimeInterval.ONE_HOUR:
            return IntervalSchedule.objects.get_or_create(
                every=1,
                period='hours',
            )[0]


class Relationship(models.Model):
    """Модель для связей таблиц базы данных."""

    related_name = models.CharField(
        max_length=50,
    )
    table = models.CharField(
        max_length=50,
    )
    through_table = models.CharField(
        max_length=50,
    )
    suffix = models.CharField(
        max_length=50,
        default='_id',
    )
    flat = models.BooleanField(
        default=False,
    )
    condition = models.CharField(
        max_length=255,
        blank=True,
    )
    process = models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        related_name='relationships',
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name='relationships',
    )

    def __str__(self) -> str:
        return f'{self.related_name} {self.through_table} {self.table}'
