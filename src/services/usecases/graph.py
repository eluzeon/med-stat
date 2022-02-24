import dataclasses
import os
import typing
from collections import defaultdict

from matplotlib.figure import Figure

import settings
from src.domain.models import Measurable
from src.domain.stats import GroupStats, StatResult
from src.graph import differ
from src.graph.differ import DiffValue
from src.graph.model import MeasurableFigures
from src.services.dao.measurements import get_all_groups_stats


@dataclasses.dataclass
class _Group:
    object: str
    left: StatResult
    right: StatResult

    @classmethod
    def from_stats(cls, groups: typing.Iterable[GroupStats]) -> typing.Iterable['_Group']:
        out = []
        o = defaultdict(dict)
        for group in groups:
            o[group.object][group.side] = group.stats
        for object_, data in o.items():
            out.append(
                _Group(
                    object=object_,
                    left=data.get("Left"),
                    right=data.get("Right")
                )
            )
        return out


def stats_to_differ_graph(groups: typing.Optional[typing.Iterable[GroupStats]] = None) -> MeasurableFigures:
    if not groups:
        groups = get_all_groups_stats()

    # словарь вида {"название метрики": [DiffValue]}
    data_map: dict[str, list[DiffValue]] = {}

    for group in _Group.from_stats(groups):
        for field in dataclasses.fields(Measurable):
            data_map.setdefault(field.name, [])
            data_map[field.name].append(
                DiffValue(
                    name=group.object,
                    right=getattr(group.right.avg.diff, field.name),
                    left=getattr(group.left.avg.diff, field.name),
                    right_err=getattr(group.right.stdev.diff, field.name),
                    left_err=getattr(group.left.stdev.diff, field.name)
                )
            )

    out_dict: dict[str, Figure] = {}
    for field, diffs in data_map.items():
        out_dict[field.lower()] = differ.build_diff_graph(
            label=field,
            values=diffs
        )

    return MeasurableFigures(**out_dict)


def build_differ_and_save(groups: typing.Iterable[GroupStats], path: typing.Optional[str] = None) -> None:
    if not path:
        path = settings.EXPORT_PATH

    figures = stats_to_differ_graph(groups)

    for name, figure in figures:
        figure.savefig(
            os.path.join(
                path, name
            ),
            dpi=settings.EXPORT_DPI
        )
