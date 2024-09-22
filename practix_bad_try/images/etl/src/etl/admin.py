from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

from django.contrib import admin
from django.db.models import QuerySet
from django.utils.html import format_html

from etl.forms import DatabaseForm, ProcessForm
from etl.models import Column, Database, Model, Process, ProcessStatus, Relationship


class ColumnInline(admin.TabularInline):
    model = Column
    autocomplete_fields = ('model', )
    extra = 0


class RelationshipInline(admin.StackedInline):
    model = Relationship
    autocomplete_fields = ('process', )
    extra = 0


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('type', 'dsn')
    search_fields = ('slug', )
    list_filter = ('type', )

    form = DatabaseForm

    @admin.display(description='dsn')
    def dsn(self, object: Database) -> str:
        """Вывод db dsn."""
        params: dict = self.form().parse_uri(object.uri)
        return format_html('<br>'.join(f'{key}={value}' for key, value in params.items()))


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'columns')
    search_fields = ('name', )
    inlines = (ColumnInline, )

    @admin.display(description='колонки')
    def columns(self, object: Model) -> str:
        """Вывод колонок модели."""
        return format_html('<br>'.join(str(column) for column in object.columns.all()))


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'process_from_table',
        'process_to_table',
        'process_status',
    )
    search_fields = (
        'slug',
        'from_table',
        'to_table',
        'source__slug',
        'target__slug',
    )
    list_filter = ('status', )
    actions = (
        'set_active_status',
        'set_disabled_status',
    )
    inlines = (RelationshipInline, )

    form = ProcessForm

    @admin.display(description='from')
    def process_from_table(self, object: Process) -> str:
        """Вывод отправителя данных ETL-процесса."""
        return f'{object.source.slug}: {object.from_table}'

    @admin.display(description='to')
    def process_to_table(self, object: Process) -> str:
        """Вывод получателя данных ETL-процесса."""
        return f'{object.target.slug}: {object.to_table}'

    @admin.display(description='task enabled', boolean=True)
    def process_status(self, object: Process) -> bool:
        """Вывод состояния ETL-процесса."""
        return object.task.enabled

    @admin.action(description='Activate selected processes')
    def set_active_status(self, request, queryset: QuerySet[Process]):
        count = queryset.count()
        process_word = 'process' if count == 1 else 'processes'
        queryset.update(status=ProcessStatus.ACTIVE)
        self.message_user(
            request,
            f'Activated {count} {process_word}',
        )

    @admin.action(description='Disable selected processes')
    def set_disabled_status(self, request, queryset: QuerySet[Process]):
        count = queryset.count()
        process_word = 'process' if count == 1 else 'processes'
        queryset.update(status=ProcessStatus.DISABLED)
        self.message_user(
            request,
            f'Disabled {count} {process_word}',
        )


admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
