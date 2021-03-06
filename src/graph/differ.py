import dataclasses
import typing
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from src.graph.utils import bartext


@dataclasses.dataclass
class DiffValue:
    name: str
    left: float
    right: float
    right_err: typing.Optional[float] = None
    left_err: typing.Optional[float] = None
    size_left: int = 0
    size_right: int = 0


def add_bartext(values: typing.Sequence[DiffValue], width: float):
    for _x, val in zip(range(len(values)), values):
        if val.size_left:
            bartext(_x, val.left, str(val.size_left), width)
        if val.size_right:
            bartext(_x, val.right, str(val.size_right), width, 'right')


def build_diff_graph(label: str, values: typing.Iterable[DiffValue],
                     right_color: typing.Optional[str] = None,
                     left_color: typing.Optional[str] = None,
                     width: typing.Optional[float] = 0.45,
                     round_digs: typing.Optional[int] = 2,
                     y_label: typing.Optional[str] = None) -> Figure:
    labels = [v.name for v in values]

    lefts = [round(v.left, round_digs) for v in values]
    left_errors = [round(v.left_err, round_digs) if v.left_err else 0 for v in values]

    rights = [round(v.right, round_digs) for v in values]
    right_errors = [round(v.right_err, round_digs) if v.right_err else 0 for v in values]

    x = np.arange(len(labels))  # the label locations

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, lefts, width, yerr=left_errors, capsize=5, label='Left', color=left_color)
    rects2 = ax.bar(x + width / 2, rights, width, yerr=right_errors, capsize=5, label='Right', color=right_color)

    add_bartext(values, width)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    if y_label:
        ax.set_ylabel(y_label)
    ax.set_title(label)
    ax.set_xticks(x, labels, rotation=70)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.set_figwidth(13)
    fig.tight_layout()

    return fig


if __name__ == '__main__':
    build_diff_graph(
        label="some",
        values=[
            DiffValue(
                name='test', left=10, right=12,
                size_left=30,
                size_right=10
            )
        ],
        y_label="[H/m]"
    ).show()
