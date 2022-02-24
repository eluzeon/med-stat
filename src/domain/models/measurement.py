import dataclasses
import datetime

from marshmallow import Schema
from marshmallow.fields import DateTime
from marshmallow_dataclass import class_schema

import settings
from src.domain.models.measurable import Measurable


@dataclasses.dataclass
class Measurement(Measurable):
    measurement_time: datetime.datetime = dataclasses.field(
        metadata={"format": settings.SCHEMA_DATETIME_FORMAT}
    )
    pattern: str
    object: str
    dominant_side: str
    position: str
    side: str
    location: str
    state: str


MeasurementSchema = class_schema(Measurement)


@dataclasses.dataclass
class Tap(Measurement):
    iteration: int


TapSchema = class_schema(Tap)
