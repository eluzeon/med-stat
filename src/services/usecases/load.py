import typing
from statistics import mean

from src.domain.exceptions import PairSetBuilderError
from src.domain.models.measurement import Measurement, Tap
from src.domain.models.measurement_pair import PairSet, GroupPairSet
from src.services.csv_reader import load_taps
from src.services.dao import memoize
from src.services.dao.measurements import save_measurements, get_filtered_measurements, object_filter, side_filter, \
    get_measurements, save_taps, GROUPS_KEY
from src.services.grouper import get_object_side_groups
from src.services.pairset_builder import SimpleOrderPairSetBuilder
from src.services.stat.func import stdev_sqrt


def load_all_measurements(rows: typing.Iterable[str]) -> typing.Iterable[Measurement]:
    """
    Загружает список строк (из csv), парсит в Measurement тип и сохраняет в памяти
    :param rows: строки или контент файла
    :return: список Measurement
    """
    taps = load_taps(rows)
    mss = taps_to_measurements(taps)
    save_measurements(mss)
    save_taps(taps)

    return mss


@memoize(GROUPS_KEY)
def get_all_groups() -> list[GroupPairSet]:
    mss = get_measurements()
    groups = get_object_side_groups(mss)
    out: list[GroupPairSet] = []

    builder = SimpleOrderPairSetBuilder()
    for group in groups:
        pairs = builder.build_pairs(group.measurements)
        if not pairs:
            raise PairSetBuilderError(f"Группа {group.object} - {group.side}: не нашлось пары до/после")

        out.append(
            GroupPairSet(
                object=group.object,
                side=group.side,
                pairset=pairs
            )
        )
    return out


def get_group_pairset(object_: str, side: str) -> PairSet:
    mss = get_filtered_measurements(
        object_filter(object_),
        side_filter(side)
    )

    builder = SimpleOrderPairSetBuilder()
    return builder.build_pairs(mss)


def safe_stdev(values: typing.Sequence[float]) -> float:
    try:
        return stdev_sqrt(values)
    except ValueError:
        return 0


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
        m = Measurement(
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
        m.frequency_error = safe_stdev([t.frequency for t in group])
        m.stiffness_error = safe_stdev([t.stiffness for t in group])
        m.decrement_error = safe_stdev([t.decrement for t in group])
        m.relaxation_error = safe_stdev([t.relaxation for t in group])
        m.creep_error = safe_stdev([t.creep for t in group])
        out.append(m)
    return out
