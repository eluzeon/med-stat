import typing
from collections import defaultdict

from src.domain.models import Measurement
from src.domain.models.measurement_pair import GroupPairSet
from src.domain.models.object_group import ObjectGroup
from src.domain.models.object_side_group import ObjectSideGroup


def group_by_object(measurements: typing.Iterable[Measurement]) -> typing.Iterable[ObjectGroup]:
    dct: dict[str, list[Measurement]] = defaultdict(list)
    for meas in measurements:
        dct[meas.object].append(meas)

    return [
        ObjectGroup(
            object=obj,
            measurements=mss
        )
        for obj, mss in dct.items()
    ]


def group_by_object_and_side(groups: typing.Iterable[ObjectGroup]) -> typing.Iterable[ObjectSideGroup]:
    lst = []
    for obj_group in groups:
        dct: dict[str, list[Measurement]] = defaultdict(list)
        for meas in obj_group.measurements:
            dct[meas.side].append(meas)

        lst.extend([
            ObjectSideGroup(
                object=obj_group.object,
                measurements=mss,
                side=side
            )
            for side, mss in dct.items()
        ])
    return lst


def get_object_side_groups(measurements: typing.Iterable[Measurement]) -> typing.Iterable[ObjectSideGroup]:
    return group_by_object_and_side(
        group_by_object(
            measurements
        )
    )
