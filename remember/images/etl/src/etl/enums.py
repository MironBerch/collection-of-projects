from django.db import models


class DatabaseType(models.TextChoices):
    """Тип базы данных."""

    SQLITE = 'sqlite'
    POSTGRESQL = 'postgresql'
    ELASTICSEARCH = 'elasticsearch'


class DataType(models.TextChoices):
    """Тип поля."""

    INT = 'int'
    STR = 'str'
    FLOAT = 'float'
    DATE = 'date'
    DATETIME = 'datetime'
    UUID = 'UUID'


class TimeInterval(models.TextChoices):
    """Временной интервал."""

    ONE_MIN = '1 minute'
    TEN_MINUTES = '10 minutes'
    ONE_HOUR = '1 hour'
    ONE_DAY = '1 day'


class ProcessStatus(models.TextChoices):
    """Статус процесса."""

    ACTIVE = 'active'
    DISABLED = 'disabled'
