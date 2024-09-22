from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

from etl_panel.forms import DatabaseForm, ProcessForm
from etl_panel.models import Column, Database, Model, Process, Relationship


class RelationshipInline(admin.StackedInline):
    """Класс для вставки связей между таблицами в админку процессов."""

    model = Relationship
    autocomplete_fields = ('process', )
    extra = 0


class ColumnInline(admin.TabularInline):
    """Класс для вставки колонок таблицы в админку модели."""

    model = Column
    autocomplete_fields = ('model', )
    extra = 0


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    """Классс админки баз данных."""

    form = DatabaseForm
    list_filter = ('type', )
    list_display = ('type', 'dsn')
    search_fields = ('slug', )

    @admin.display
    def dsn(self, object: Database) -> str:
        """Вывод настроек подключения к базам данных."""
        params = self.form().parse_uri(object.uri, object.type)
        return format_html('<br>'.join(f'{key}={value}' for key, value in params.items()))


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    """Класс админки моделей."""

    inlines = (ColumnInline,)
    search_fields = ('title',)
    list_display = ('title', 'columns')

    @admin.display
    def columns(self, object: Model) -> str:
        """Вывод колонок модели."""
        return format_html('<br>'.join(str(col) for col in object.columns.all()))


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    """Класс админки процессов."""

    form = ProcessForm
    inlines = (RelationshipInline,)
    search_fields = ('slug', 'source', 'target')
    list_filter = ('source', 'target')
    list_display = ('slug', 'from_', 'to', 'active')
    exclude = ('task', )

    @admin.display(description='from')
    def from_(self, object: Process) -> str:
        """Вывод отправителя данных ETL-процесса."""
        return f'{object.source.slug}: {object.from_table}'

    @admin.display
    def to(self, object: Process):
        """Вывод получателя данных ETL-процесса."""
        return f'{object.target.slug}: {object.to_table}'

    @admin.display(boolean=True)
    def active(self, object: Process) -> bool:
        """Вывод состояния ETL-процесса."""
        return object.task.enabled


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
