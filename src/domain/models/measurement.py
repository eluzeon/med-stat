import dataclasses
import datetime

from marshmallow_dataclass import class_schema

from src.domain.models.measurable import Measurable
from src.domain.schemas import MeasurementBaseSchema


@dataclasses.dataclass
class Measurement(Measurable):
    measurement_time: datetime.datetime
    pattern: str
    object: str
    dominant_side: str
    position: str
    side: str
    location: str
    state: str


MeasurementSchema = class_schema(Measurement, base_schema=MeasurementBaseSchema)


@dataclasses.dataclass
class Tap(Measurement):
    iteration: int


TapSchema = class_schema(Tap, base_schema=MeasurementBaseSchema)
