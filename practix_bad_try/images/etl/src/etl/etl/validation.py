import builtins
import datetime
import uuid
from typing import Any, Type

import pandas
from dateutil import parser
from pydantic import BaseModel, Field, ValidationError, create_model, validator
from pydantic.fields import FieldInfo

from django.db.models.query import QuerySet
from django.forms.models import model_to_dict

from etl.etl.errors import TransformError
from etl.models import Column, Model, Relationship


class Validation(BaseModel):
    """ETL-сервис валидации и трансформации данных."""

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @classmethod
    @validator('*', pre=True)
    def transform_default_value(cls, value: Any, field: FieldInfo) -> Any:
        """
        Преобразование пустых значений в значения по умолчанию.

        :arg value: Значение поля
        :arg field: Метаданные поля

        :return Any: Значение после валидации
        """

        if not isinstance(value, list):
            return field.default if pandas.isna(value) else value
        return value

    @classmethod
    def get_schema(cls, model: Model, relations: QuerySet[Relationship]) -> Type['Validation']:
        """
        Получение динамической схемы для валидации данных.

        :arg model: Модель объекта
        :arg relations: Данные о вложенных объектах

        :return Type[Validation]: Схема валидации данных
        """

        fields = cls.get_fields(model)
        for rel in relations:
            if not rel.flat:
                nested_type = create_model(
                    rel.model.name,
                    __base__=cls,
                    **cls.get_fields(rel.model),
                )
            else:
                nested_type = cls.get_type(rel.model.columns.first().type)
            fields[rel.related_name] = list[nested_type], Field(default=[])
        return create_model(model.name, __base__=cls, **fields)

    @classmethod
    def get_fields(cls, model: Model) -> dict:
        """
        Определение полей схемы.

        :arg model: Модель объекта

        :return dict: Поля схемы
        """

        mapping = {}
        for col in model.columns.all():
            mapping[col.name] = cls.get_type(col.type), cls.get_field_info(col)
        return mapping

    @classmethod
    def get_type(cls, value: str) -> Type:
        """
        Приведение строкового представления типа данных в тип данных Python.

        :arg value: Строковое представление типа данных

        :return Type: Тип данных Python
        """

        if value == 'UUID':
            return getattr(uuid, value)
        if value in {'date', 'datetime'}:
            return getattr(datetime, value)
        else:
            return getattr(builtins, value)

    @classmethod
    def get_field_info(cls, column: Column) -> FieldInfo:
        """
        Получение метаданных поля схемы.

        :arg column: Колонка модели

        :return FieldInfo: Метаданные поля
        """

        field_info = model_to_dict(column)
        if default_value := field_info.pop('default', None):
            if default_value == 'None':
                field_info['default'] = None
            elif default_value in {'""', "''"}:
                field_info['default'] = ''
            else:
                field_info['default'] = default_value
        return Field(**field_info)

    @classmethod
    def validate_row(cls, row: pandas.Series) -> dict:
        """
        Основной метод валидции строк в датафрейме.

        :arg row: Одномерный массив значений датафрейма

        :raise TransformError: Ошибка трансформации данных

        :return dict: Строка после обработки
        """

        dict_row = {key: value for key, value in row.to_dict().items() if value is not None}
        for key, value in dict_row.items():
            if isinstance(value, str):
                try:
                    dt = parser.isoparse(value)
                    dict_row[key] = dt.isoformat()
                except ValueError:
                    pass
        try:
            data = pandas.Series(cls(**dict_row).model_dump(by_alias=True))
        except ValidationError as exc:
            raise TransformError(exc.errors(), str(row.name))
        return data
