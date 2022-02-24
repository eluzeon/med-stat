import dataclasses
import datetime
import typing

from src.domain.models import Measurement


@dataclasses.dataclass
class MeasurementPair:
    date: datetime.date
    object: str
    side: str
    before: Measurement
    after: Measurement


PairSet = typing.Iterable[MeasurementPair]


@dataclasses.dataclass
class GroupPairSet:
    object: str
    side: str
    pairset: PairSet
