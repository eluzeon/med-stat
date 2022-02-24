from src.domain.models import Measurable
from src.domain.models.measurement_pair import MeasurementPair
from src.services.stat.func import pdiff


def diff(pair: MeasurementPair) -> Measurable:
    return Measurable(
        frequency=pdiff(pair.before.frequency, pair.after.frequency),
        stiffness=pdiff(pair.before.stiffness, pair.after.stiffness),
        decrement=pdiff(pair.before.decrement, pair.after.decrement),
        relaxation=pdiff(pair.before.decrement, pair.after.relaxation),
        creep=pdiff(pair.before.creep, pair.after.creep)
    )
