import builtins
import datetime
import logging
import uuid
from typing import Any, Type

import pandas
from pydantic import BaseModel, Field, create_model, validator
from pydantic.fields import FieldInfo

from django.db.models.query import QuerySet
from django.forms.models import model_to_dict

from etl_panel.models import Column, Model, Relationship

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


class Validation(BaseModel):
    """ETL-сервис валидации и трансформации данных."""

    class Config:
        """Настройки валидации."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    @classmethod
    @validator('*', pre=True)
    def transform_default_value(cls, value: Any, field) -> Any:
        """Преобразование пустых значений в значения по умолчанию."""
        if not isinstance(value, list):
            return field.default if pandas.isna(value) else value
        return value

    @classmethod
    def get_schema(cls, model: Model, relations: QuerySet[Relationship]) -> Type['Validation']:
        """Получение динамической схемы для валидации данных."""
        fields = cls.get_fields(model)
        for rel in relations:
            if not rel.flat:
                nested_type = create_model(
                    rel.model.title,
                    __base__=cls,
                    **cls.get_fields(rel.model),
                )
            else:
                nested_type = cls.get_type(rel.model.columns.first().type)
            fields[rel.related_name] = list[nested_type], Field(default=[])
        return create_model(model.title, __base__=cls, **fields)

    @classmethod
    def get_fields(cls, model: Model) -> dict:
        """Определение полей схемы."""
        mapping = {}
        for col in model.columns.all():
            mapping[col.name] = cls.get_type(col.type), cls.get_field_info(col)
        return mapping

    @classmethod
    def get_type(cls, value: str) -> Type:
        """Приведение строкового представления типа данных в тип данных Python."""
        if value == 'UUID':
            return getattr(uuid, value)
        if value in {'date', 'datetime'}:
            return getattr(datetime, value)
        else:
            return getattr(builtins, value)

    @classmethod
    def get_field_info(cls, column: Column) -> FieldInfo:
        """Получение метаданных поля схемы."""
        field_info = model_to_dict(column)
        default_value = field_info.pop('default', None)
        if default_value is not None:
            if default_value == 'None':
                field_info['default'] = None
            elif default_value in {'""', "''"}:
                field_info['default'] = ''
            else:
                field_info['default'] = default_value
        return Field(**field_info)

    @classmethod
    def validate_row(cls, row: pandas.Series) -> dict:
        """Основной метод валидции строк в датафрейме."""
        try:
            data = pandas.Series(cls(**row).model_dump(by_alias=True))
        except Exception as exception:
            logging.error(f'Row name: `{str(row.name)}` Create error: `{exception}`')
        return data
