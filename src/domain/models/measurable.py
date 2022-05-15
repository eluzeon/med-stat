import dataclasses


@dataclasses.dataclass
class Measurable:
    frequency: float
    stiffness: float
    decrement: float
    relaxation: float
    creep: float

    def __post_init__(self):
        """
        Что это?)
        требование изменилось под конец,
        если просто добавить поля в датакласс - все полетит)
        """
        self.frequency_error: float = 0
        self.stiffness_error: float = 0
        self.decrement_error: float = 0
        self.relaxation_error: float = 0
        self.creep_error: float = 0


def get_measurable_field_names() -> list[str]:
    return [f.name for f in dataclasses.fields(Measurable)]


measurable_fields = get_measurable_field_names()
