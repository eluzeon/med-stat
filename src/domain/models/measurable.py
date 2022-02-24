import dataclasses


@dataclasses.dataclass
class Measurable:
    frequency: float
    stiffness: float
    decrement: float
    relaxation: float
    creep: float
