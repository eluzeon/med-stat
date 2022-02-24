import statistics
import typing

from src.domain.models.measurement_pair import PairSet, MeasurementPair


def avg_calc(collection: PairSet, key: typing.Callable[[MeasurementPair], float]) -> float:
    values = list(map(key, collection))
    return statistics.mean(values)


def stdev_calc(collection: PairSet, key: typing.Callable[[MeasurementPair], float]) -> float:
    values = list(map(key, collection))
    return statistics.stdev(values)


def diff(value1: float, value2: float) -> float:
    return value2 - value1


def pdiff(value1: float, value2: float) -> float:
    return diff(value1, value2) * 100 / value2
