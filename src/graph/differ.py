import dataclasses
import typing
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


@dataclasses.dataclass
class DiffValue:
    name: str
    left: float
    right: float
    right_err: typing.Optional[float] = None
    left_err: typing.Optional[float] = None


def build_diff_graph(label: str, values: typing.Iterable[DiffValue],
                     right_color: typing.Optional[str] = None,
                     left_color: typing.Optional[str] = None,
                     width: typing.Optional[float] = 0.35,
                     round_digs: typing.Optional[int] = 2) -> Figure:
    labels = [v.name for v in values]

    lefts = [round(v.left, round_digs) for v in values]
    left_errors = [round(v.left_err, round_digs) for v in values if v.left_err]

    rights = [round(v.right, round_digs) for v in values]
    right_errors = [round(v.right_err, round_digs) for v in values if v.right_err]

    x = np.arange(len(labels))  # the label locations

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, lefts, width, yerr=left_errors, capsize=5, label='Left', color=left_color)
    rects2 = ax.bar(x + width / 2, rights, width, yerr=right_errors, capsize=5, label='Right', color=right_color)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(label)
    ax.set_title(label)
    ax.set_xticks(x, labels, rotation=70)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    fig.set_figwidth(13)

    return fig
