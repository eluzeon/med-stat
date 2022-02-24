import typing
from statistics import mean

from src.domain.models.measurement import Measurement, Tap
from src.domain.models.measurement_pair import PairSet, GroupPairSet
from src.services.csv_reader import load_taps
from src.services.dao.measurements import save_measurements, get_filtered_measurements, object_filter, side_filter, \
    get_measurements, save_all_groups
from src.services.grouper import get_object_side_groups
from src.services.pairset_builder import SimpleOrderPairSetBuilder


def load_all_measurements(rows: typing.Iterable[str]) -> typing.Iterable[Measurement]:
    """
    Загружает список строк (из csv), парсит в Measurement тип и сохраняет в памяти
    :param rows: строки или контент файла
    :return: список Measurement
    """
    mss = taps_to_measurements(load_taps(rows))
    save_measurements(mss)

    return mss


def get_all_groups() -> list[GroupPairSet]:
    mss = get_measurements()
    groups = get_object_side_groups(mss)
    out: list[GroupPairSet] = []

    builder = SimpleOrderPairSetBuilder()
    for group in groups:
        out.append(
            GroupPairSet(
                object=group.object,
                side=group.side,
                pairset=builder.build_pairs(group.measurements)
            )
        )

    save_all_groups(out)

    return out


def get_group_pairset(object_: str, side: str) -> PairSet:
    mss = get_filtered_measurements(
        object_filter(object_),
        side_filter(side)
    )

    builder = SimpleOrderPairSetBuilder()
    return builder.build_pairs(mss)


def taps_to_measurements(taps: typing.Iterable[Tap]) -> list[Measurement]:
    """
    Усредняет тапы и объединяет их в одно исследование
    """
    # предполагается, что тапы отсортированы по времени,
    # поэтому мы можем просто собрать все тапы последовательно в 1 исследование
    prev_iter = 0
    group: list[Measurement] = []
    groups: list[list[Measurement]] = []
    for tap in taps:
        if tap.iteration < prev_iter:
            prev_iter = 0
            groups.append(group)
            group = [tap]
            continue

        group.append(tap)
        prev_iter = tap.iteration

    if group:
        groups.append(group)

    out: list[Measurement] = []
    for group in groups:
        tap = group[0]
        out.append(
            Measurement(
                frequency=mean(t.frequency for t in group),
                stiffness=mean(t.stiffness for t in group),
                decrement=mean(t.decrement for t in group),
                relaxation=mean(t.relaxation for t in group),
                creep=mean(t.creep for t in group),
                measurement_time=tap.measurement_time,
                pattern=tap.pattern,
                object=tap.object,
                dominant_side=tap.dominant_side,
                position=tap.position,
                side=tap.side,
                location=tap.location,
                state=tap.state,
            )
        )
    return out