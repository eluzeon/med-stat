import dataclasses
import typing

from src.domain.models import Measurable
from src.domain.models.measurement_pair import PairSet, MeasurementPair
from src.domain.stats import Stat, StatResult
from src.services.stat.func import avg_calc, stdev_calc
from src.services.stat.pair import diff


def _build_measurable(pairset: PairSet,
                      key: typing.Callable[[MeasurementPair], Measurable],
                      calc_fn: typing.Callable[[PairSet, typing.Callable[[MeasurementPair], float]], float]) -> Measurable:
    kws = {}
    for field in dataclasses.fields(Measurable):
        fname = field.name
        fvalue = calc_fn(pairset, lambda x: getattr(key(x), fname))
        kws[fname] = fvalue
    return Measurable(**kws)


def _avg_stats(pairset: PairSet) -> Stat:
    return Stat(
        after=_build_measurable(pairset, key=lambda x: x.after, calc_fn=avg_calc),
        before=_build_measurable(pairset, key=lambda x: x.before, calc_fn=avg_calc),
        diff=_build_measurable(pairset, key=lambda x: diff(x), calc_fn=avg_calc)
    )


def _stdev_stats(pairset: PairSet) -> Stat:
    return Stat(
        after=_build_measurable(pairset, key=lambda x: x.after, calc_fn=stdev_calc),
        before=_build_measurable(pairset, key=lambda x: x.before, calc_fn=stdev_calc),
        diff=_build_measurable(pairset, key=lambda x: diff(x), calc_fn=stdev_calc)
    )


def calc_stats(pairset: PairSet) -> StatResult:
    return StatResult(
        avg=_avg_stats(pairset),
        stdev=_stdev_stats(pairset)
    )
