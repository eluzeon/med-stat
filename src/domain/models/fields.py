import enum


class MeasurableField(str, enum.Enum):
    FREQUENCY = 'frequency'
    STIFFNESS = 'stiffness'
    DECREMENT = 'decrement'
    RELAXATION = 'relaxation'
    CREEP = 'creep'

    def __str__(self) -> str:
        return self.value
