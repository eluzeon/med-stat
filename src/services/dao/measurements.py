import datetime
import typing

from src import store
from src.domain.models import Measurement, Tap
from src.domain.models.measurement_pair import GroupPairSet
from src.domain.stats import GroupStats

LIST_KEY = "measurement_list"
GROUPS_KEY = "all_groups_list"
GROUPS_STATS = "all_groups_stats"
TAP_LIST_KEY = "all_taps_list"

Filter = typing.Callable[[Measurement], bool]


def object_filter(object_: str) -> Filter:
    return lambda it: it.object == object_


def side_filter(side_: str) -> Filter:
    return lambda it: it.side == side_


def date_filter(date: datetime.date) -> Filter:
    return lambda it: it.measurement_time.date() == date


def save_measurements(measurements: typing.Iterable[Measurement]) -> None:
    store.push(LIST_KEY, measurements)


def save_taps(taps: typing.Iterable[Tap]) -> None:
    store.push(TAP_LIST_KEY, taps)


def get_measurements() -> list[Measurement]:
    val = store.get(LIST_KEY)
    if val is None:
        return []

    # force cast to list
    return list(val)


def get_filtered_measurements(*filters: Filter) -> typing.Iterable[Measurement]:
    measurements = get_measurements()
    return [
        meas
        for meas in measurements
        if all(flt(meas) for flt in filters)
    ]


def save_all_groups(groups: list[GroupPairSet]) -> None:
    store.push(
        GROUPS_KEY,
        groups
    )


def save_all_groups_stats(groups: list[GroupStats]) -> None:
    store.push(
        GROUPS_STATS,
        groups
    )


def get_all_groups_stats() -> list[GroupStats]:
    return store.get(GROUPS_STATS)


def get_all_groups() -> list[GroupPairSet]:
    return store.get(GROUPS_KEY)
