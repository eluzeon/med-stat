import dataclasses


@dataclasses.dataclass
class Measurable:
    frequency: float
    stiffness: float
    decrement: float
    relaxation: float
    creep: float


def get_measurable_field_names() -> list[str]:
    return [f.name for f in dataclasses.fields(Measurable)]
