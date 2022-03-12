from src.domain.models import Measurable
from src.domain.models.measurement_pair import MeasurementPair
from src.services.stat.func import pdiff_rev


def diff(pair: MeasurementPair) -> Measurable:
    return Measurable(
        frequency=pdiff_rev(pair.before.frequency, pair.after.frequency),
        stiffness=pdiff_rev(pair.before.stiffness, pair.after.stiffness),
        decrement=pdiff_rev(pair.before.decrement, pair.after.decrement),
        relaxation=pdiff_rev(pair.before.relaxation, pair.after.relaxation),
        creep=pdiff_rev(pair.before.creep, pair.after.creep)
    )
