import dataclasses
import os
import typing
from collections import defaultdict
from statistics import mean

from matplotlib import pyplot as plt
from matplotlib.figure import Figure

import settings
from src.domain.models import Measurable
from src.domain.models.measurable import get_measurable_field_names, measurable_fields
from src.domain.models.measurement_pair import GroupPairSet
from src.domain.models.object_side_group import ObjectSideGroup
from src.domain.stats import GroupStats, StatResult
from src.graph import differ
from src.graph.differ import DiffValue
from src.graph.dots import build_dots_graph, DotValue
from src.graph.model import MeasurableFigures
from src.services.dao.measurements import get_all_groups_stats


T = typing.TypeVar("T")

@dataclasses.dataclass()
class AnyObjectSide(typing.Protocol):
    object: str
    side: str


K = typing.TypeVar("K", bound=AnyObjectSide)


@dataclasses.dataclass
class ObjectGroup(typing.Generic[T]):
    object: str
    left: T
    right: T

    @classmethod
    def build(cls, objects: typing.Iterable[K],
              getter: typing.Callable[[K], T]) -> typing.Iterable["ObjectGroup[T]"]:
        out = []
        o: dict[str, dict[str, T]] = defaultdict(dict)
        for group in objects:
            o[group.object][group.side] = getter(group)
        for object_, data in o.items():
            out.append(
                ObjectGroup(
                    object=object_,
                    left=data.get("Left"),
                    right=data.get("Right")
                )
            )
        return out


def stats_to_differ_graph(groups: typing.Optional[typing.Iterable[GroupStats]] = None,
                          save_immediate: bool = False,
                          save_path: typing.Optional[str] = None) -> MeasurableFigures:
    if not groups:
        groups = get_all_groups_stats()

    # словарь вида {"название метрики": [DiffValue]}
    data_map: dict[str, list[DiffValue]] = {}

    for group in ObjectGroup.build(groups, lambda x: x.stats):
        for field in dataclasses.fields(Measurable):
            data_map.setdefault(field.name, [])
            data_map[field.name].append(
                DiffValue(
                    name=group.object,
                    right=getattr(group.right.avg.diff, field.name),
                    left=getattr(group.left.avg.diff, field.name),
                    right_err=getattr(group.right.stdev.diff, field.name),
                    left_err=getattr(group.left.stdev.diff, field.name),
                    size_left=group.left.size,
                    size_right=group.right.size
                )
            )

    out_dict: dict[str, Figure] = {}
    for field, diffs in data_map.items():
        fig = differ.build_diff_graph(
            label=field,
            values=diffs
        )
        if save_immediate:
            fig.savefig(
                os.path.join(
                    save_path, field.lower()
                ),
                dpi=settings.EXPORT_DPI_MAX
            )
            # close plots for free memory
            plt.close("all")
        else:
            out_dict[field.lower()] = fig

    # return MeasurableFigures(**out_dict)


def build_differ_and_save(groups: typing.Iterable[GroupStats], path: typing.Optional[str] = None) -> None:
    if not path:
        path = settings.EXPORT_PATH

    stats_to_differ_graph(groups, save_immediate=True, save_path=path)


def single_pairset_to_detailed_graph(group: GroupPairSet) -> list[tuple[str, Figure]]:
    pack = []
    for attr in get_measurable_field_names():
        before_values = [getattr(mp.before, attr) for mp in group.pairset]
        before_errors = [getattr(mp.before, f"{attr}_error") for mp in group.pairset]
        after_values = [getattr(mp.after, attr) for mp in group.pairset]
        after_errors = [getattr(mp.after, f"{attr}_error") for mp in group.pairset]
        times = [mp.before.measurement_time for mp in group.pairset]

        title = f"{group.object} {group.side} - {attr}"

        fig = build_dots_graph(
            DotValue(
                values=before_values,
                values_err=before_errors,
                title="Before"
            ),
            DotValue(
                values=after_values,
                values_err=after_errors,
                title="After"
            ),
            xs=[t.strftime("%d.%m.%y %H:%M") for t in times],
            title=title
        )
        pack.append((title, fig))
    return pack


def pairset_groups_to_detailed_graph(groups: typing.Iterable[GroupPairSet],
                                     save_immediate: bool = True,
                                     save_path: typing.Optional[str] = None) -> list[tuple[str, Figure]]:
    out = []
    for group in groups:
        pack = single_pairset_to_detailed_graph(group)
        if save_immediate:
            for name, fig in pack:
                fig.savefig(
                    os.path.join(
                        save_path, name
                    ),
                    dpi=settings.EXPORT_DPI_MIN
                )
                # close figure, to clean memory
                plt.close('all')
    return out


def build_detail_graphs_and_save(groups: typing.Iterable[GroupPairSet], path: typing.Optional[str] = None) -> None:
    if not path:
        path = settings.EXPORT_PATH

    pairset_groups_to_detailed_graph(groups, save_immediate=True, save_path=path)


def build_mean_graphs_and_save(groups: typing.Iterable[ObjectSideGroup], path: typing.Optional[str] = None) -> None:
    if not path:
        path = settings.EXPORT_PATH

    final_groups = ObjectGroup.build(groups, lambda x: x.measurements)
    for field in measurable_fields:
        values = []
        for group in final_groups:
            l_mss: typing.Sequence[Measurable] = group.left
            r_mss: typing.Sequence[Measurable] = group.right

            values.append(
                DiffValue(
                    name=group.object,
                    left=mean(getattr(l, field) for l in l_mss) if l_mss else 0,
                    right=mean(getattr(r, field) for r in r_mss) if r_mss else 0,
                    left_err=mean(getattr(l, f"{field}_error") for l in l_mss) if l_mss else 0,
                    right_err=mean(getattr(r, f"{field}_error") for r in r_mss) if r_mss else 0,
                    size_right=len(r_mss) if r_mss else 0,
                    size_left=len(l_mss) if l_mss else 0
                )
            )

        fig = differ.build_diff_graph(
            label=field,
            values=values
        )
        fig.savefig(
            os.path.join(
                path, field
            ),
            dpi=settings.EXPORT_DPI_MAX
        )
        plt.close("all")
