import dataclasses
import datetime
import typing

from marshmallow_dataclass import class_schema

from src.domain.models import Measurement


@dataclasses.dataclass
class MeasurementPair:
    date: datetime.date
    object: str
    side: str
    before: Measurement
    after: Measurement


MeasurementPairSchema = class_schema(MeasurementPair)
PairSet = typing.Iterable[MeasurementPair]


@dataclasses.dataclass
class GroupPairSet:
    object: str
    side: str
    pairset: PairSet
