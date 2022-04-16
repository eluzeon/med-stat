import datetime
import typing

from marshmallow import Schema, ValidationError
from marshmallow.fields import DateTime, Float

import settings


class MultiDateTimeField(DateTime):
    DEFAULT_FORMATS = settings.SCHEMA_DATETIME_FORMATS

    def __init__(self, formats: typing.Optional[list[str]] = None, **kwargs):
        self.formats = formats or self.DEFAULT_FORMATS
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        for format_ in self.formats:
            try:
                self.format = format_
                return super()._deserialize(value, attr, data, **kwargs)
            except ValidationError:
                continue

        raise self.fail('Not a valid datetime')


class CustomFloatField(Float):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Optional[int]:
        value = value.replace(",", ".")
        return super()._deserialize(value, attr, data, **kwargs)


class MeasurementBaseSchema(Schema):
    TYPE_MAPPING = {
        datetime.datetime: MultiDateTimeField,
        float: CustomFloatField
    }
