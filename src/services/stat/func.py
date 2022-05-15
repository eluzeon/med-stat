import math
import statistics
import typing

from src.domain.models.measurement_pair import PairSet, MeasurementPair


def avg_calc(collection: PairSet, key: typing.Callable[[MeasurementPair], float]) -> float:
    values = list(map(key, collection))
    return statistics.mean(values)


def stdev_sqrt(values: typing.Sequence[float]) -> float:
    try:
        return statistics.stdev(values) / math.sqrt(len(values))
    except statistics.StatisticsError:
        return 0


def stdev_calc(collection: PairSet, key: typing.Callable[[MeasurementPair], float]) -> float:
    values = list(map(key, collection))
    return stdev_sqrt(values)


def diff(value1: float, value2: float) -> float:
    return value1 - value2


def pdiff(value1: float, value2: float) -> float:
    return diff(value1, value2) * 100 / value2


def pdiff_rev(before_value: float, after_value: float) -> float:
    return pdiff(after_value, before_value)
