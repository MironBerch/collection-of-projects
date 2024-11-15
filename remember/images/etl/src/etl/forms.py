from re import findall
from typing import Any
from urllib.parse import parse_qs, urlparse

from django import forms
from django.core.validators import EMPTY_VALUES

from etl.models import Database, Process
from etl.validators import validate_integer_and_positive


class DatabaseForm(forms.ModelForm):
    """Форма базы данных."""

    host = forms.CharField(max_length=255, required=False)
    port = forms.CharField(required=False, validators=[validate_integer_and_positive])
    dbname = forms.CharField(max_length=255, required=False)
    user = forms.CharField(max_length=255, required=False)
    password = forms.CharField(max_length=255, required=False)
    schema = forms.CharField(max_length=255, required=False)
    file_path = forms.CharField(max_length=255, required=False)

    URI_TEMPLATES = {
        'sqlite': 'sqlite:///file:{file_path}?mode=rw&uri=true',
        'postgresql': (
            'postgresql://{user}:{password}@{host}:{port}/'
            '{dbname}?options=-c search_path={schema}'
        ),
        'elasticsearch': '{host}:{port}',
    }

    def __init__(self, *args, **kwargs):
        if instance := kwargs.get('instance'):
            kwargs['initial'] = self.parse_uri(instance.uri)
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        if db_type := self.cleaned_data.get('type'):
            required_fields = findall(r'{(.*?)}', self.URI_TEMPLATES[db_type])
            for field, value in self.cleaned_data.items():
                if field in required_fields and value in EMPTY_VALUES:
                    self._errors[field] = self.error_class(['This field is required.'])
        return super().clean()

    def save(self, commit=True) -> Database:
        instance: Database = super(DatabaseForm, self).save(commit=False)
        instance.uri = self.URI_TEMPLATES[instance.type].format(**self.cleaned_data)
        return super().save(commit=commit)

    def parse_uri(self, uri: str) -> dict[str, str]:
        parsed_uri = urlparse(uri)
        dsn: dict[str, str | int] = {
            'host': parsed_uri.hostname,
            'port': parsed_uri.port,
            'user': parsed_uri.username,
            'password': parsed_uri.password,
        }
        query_params = parse_qs(parsed_uri.query)
        if parsed_uri.scheme.startswith(('elastic')):
            dsn['host'] = parsed_uri.scheme
            dsn['port'] = parsed_uri.path
        if parsed_uri.scheme.startswith(('postgresql')):
            dsn['dbname'] = parsed_uri.path.lstrip('/').split('/')[-1]
            options = query_params.get('options', [''])[0]
            if 'search_path=' in options:
                dsn['schema'] = options.split('search_path=')[-1].split('&')[0]
        if parsed_uri.scheme.startswith(('sqlite')):
            dsn['file_path'] = parsed_uri.path[6:]
        return {key: value for key, value in dsn.items() if value is not None}

    class Meta:
        model = Database
        fields = (
            'slug',
            'type',
            'host',
            'port',
            'dbname',
            'user',
            'password',
            'schema',
            'file_path',
        )
        widgets = {
            'type': forms.Select(
                attrs={
                    '--hideshow-fields': 'host, port, file_path, dbname, user, password, schema',
                    '--show-on-sqlite': 'file_path',
                    '--show-on-postgresql': 'host, port, dbname, user, password, schema',
                    '--show-on-elasticsearch': 'host, port',
                },
            ),
        }

    class Media:
        """Настройки для динамической формы."""

        js = ('https://cdn.jsdelivr.net/gh/scientifichackers/django-hideshow@0.0.1/hideshow.js', )


class ProcessForm(forms.ModelForm):
    """Форма модели процесса для показа поля выбора интервала времени при отметке синхронизации."""

    class Meta:
        model = Process
        fields = (
            'slug',
            'source',
            'target',
            'status',
            'from_table',
            'to_table',
            'model',
            'index_column',
            'sync',
            'time_interval',
        )
        widgets = {
            'sync': forms.CheckboxInput(
                attrs={
                    '--hideshow-fields': 'time_interval',
                    '--show-on-checked': 'time_interval',
                },
            ),
        }

    class Media:
        """Настройки для динамической формы."""

        js = ('https://cdn.jsdelivr.net/gh/scientifichackers/django-hideshow@0.0.1/hideshow.js', )
