from django.db import models


class DataType(models.TextChoices):
    """Тип данных."""

    str = 'str', 'str'
    int = 'int', 'int'
    float = 'float', 'float'
    date = 'date', 'date'
    datetime = 'datetime', 'datetime'
    UUID = 'UUID', 'UUID'


class DatabaseType(models.TextChoices):
    """Тип базы данных."""

    sqlite = 'sqlite', 'sqlite'
    postgresql = 'postgresql', 'postgresql'
    elasticsearch = 'elasticsearch', 'elasticsearch'


class TimeInterval(models.TextChoices):
    """Времененной интервал."""

    ONE_MINUTE = '1 minute', '1 minute'
    FIVE_MINUTES = '5 minutes', '5 minutes'
    ONE_HOUR = '1 hour', '1 hour'


class ProcessStatus(models.TextChoices):
    """Статус процесса."""

    ACTIVE = 'active', 'active'
    DISABLED = 'disabled', 'disabled'
