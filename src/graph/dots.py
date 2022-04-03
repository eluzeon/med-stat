import dataclasses
import itertools
import typing

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import settings


@dataclasses.dataclass
class DotValue:
    values: list[float]
    title: str

    def __len__(self) -> int:
        return len(self.values)


def build_dots_graph(*values: DotValue,
                     xs: list[str],
                     title: str,
                     colors: typing.Optional[list[str]] = None) -> Figure:
    if not colors:
        colors = settings.DOT_GRAPH_COLORS

    color_piker = itertools.cycle(colors)
    fig, ax = plt.subplots()
    x = list(range(0, len(values[0])))

    for val in values:
        c = next(color_piker)
        ax.plot(x, val.values, f'o-{c}', label=val.title)

    ax.legend()
    ax.set_title(title)
    ax.set_xticks(x, xs, rotation=70)

    fig.tight_layout()
    return fig


if __name__ == '__main__':
    build_dots_graph(
        DotValue([12, 13, 10, 12, 10, 13], "test 1"),
        DotValue([10, 11, 10, 12, 10, 11], "test 2"),
        xs=["21/01", "22/01", "23/01", "24/01", "25/01", '26/01'],
        title="Stiffness"
    )
