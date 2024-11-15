import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from django.db import models
from django.utils import timezone

from etl.enums import DatabaseType, DataType, ProcessStatus, TimeInterval


class Database(models.Model):
    """База данных."""

    slug = models.SlugField(unique=True)
    type = models.CharField(
        verbose_name='тип',
        max_length=13,
        choices=DatabaseType.choices,
    )
    uri = models.CharField(
        max_length=255,
    )

    def __str__(self) -> str:
        return self.slug


class Model(models.Model):
    """Cхема данных."""

    name = models.CharField(
        verbose_name='название',
        unique=True,
        max_length=255,
    )

    def __str__(self) -> str:
        return self.name


class Column(models.Model):
    """Колонка модели базы данных."""

    name = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    type = models.CharField(
        verbose_name='тип данных',
        max_length=8,
        choices=DataType.choices,
    )
    default = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name='значение по умолчанию',
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name='columns',
        verbose_name='модель частью которой является колонка',
    )

    def __str__(self) -> str:
        return f'{self.name}: {self.type.upper()}'


class Process(models.Model):
    """Процесса передачи данных."""

    slug = models.SlugField(unique=True)
    status = models.CharField(
        choices=ProcessStatus.choices,
        default=ProcessStatus.ACTIVE,
        max_length=8,
        verbose_name='task status',
    )
    source = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
        related_name='targets',
        verbose_name='исходная бд',
    )
    target = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
        related_name='sources',
        verbose_name='целевая бд',
    )
    time_interval = models.CharField(
        choices=TimeInterval.choices,
        default=TimeInterval.ONE_MIN,
        max_length=10,
        verbose_name='интервал',
    )
    sync = models.BooleanField(
        default=False,
        verbose_name='синхронизировать данные',
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        verbose_name='модель с которой связан процесс',
    )
    from_table = models.CharField(max_length=255)
    to_table = models.CharField(max_length=255)
    index_column = models.CharField(
        max_length=255,
        default='id',
        verbose_name='первичный ключ',
    )
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
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
            args=json.dumps([self.pk]),
            start_time=timezone.now(),
            one_off=self.sync,
        )
        self.save()

    @property
    def interval_schedule(self) -> IntervalSchedule:
        """Свойство для получения интервала времени."""
        if self.time_interval == TimeInterval.ONE_MIN:
            return IntervalSchedule.objects.get_or_create(every=1, period='minutes')[0]
        if self.time_interval == TimeInterval.TEN_MINUTES:
            return IntervalSchedule.objects.get_or_create(every=10, period='minutes')[0]
        if self.time_interval == TimeInterval.ONE_HOUR:
            return IntervalSchedule.objects.get_or_create(every=1, period='hours')[0]
        if self.time_interval == TimeInterval.ONE_DAY:
            return IntervalSchedule.objects.get_or_create(every=1, period='days')[0]


class Relationship(models.Model):
    """Связей таблиц базы данных."""

    related_name = models.CharField(max_length=50)
    table = models.CharField(
        max_length=50,
        verbose_name='таблица'
    )
    through_table = models.CharField(
        max_length=50,
        verbose_name='промежуточная таблица'
    )
    suffix = models.CharField(
        max_length=25,
        default='_id',
    )
    flat = models.BooleanField(
        default=False,
        verbose_name='храниться ли связанные данные в одной таблице',
    )
    condition = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='условие',
    )
    process = models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        related_name='relationships',
        verbose_name='процесс',
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        related_name='relationships',
        verbose_name='модель',
    )

    def __str__(self) -> str:
        return self.related_name
