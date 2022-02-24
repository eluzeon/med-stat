import dataclasses
import typing

from matplotlib.figure import Figure


@dataclasses.dataclass
class MeasurableFigures:
    frequency: Figure
    stiffness: Figure
    decrement: Figure
    relaxation: Figure
    creep: Figure

    def __iter__(self) -> typing.Iterable[tuple[str, Figure]]:
        for field in dataclasses.fields(self):
            yield field.name, getattr(self, field.name)
