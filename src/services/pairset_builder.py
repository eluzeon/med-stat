import abc
import dataclasses
import datetime
import typing

import settings
from src.domain.models import Measurement
from src.domain.models.measurement_pair import PairSet, MeasurementPair
from src.utils import last


class PairSetBuilder(abc.ABC):
    def build_pairs(self, mss: typing.Iterable[Measurement]) -> PairSet:
        raise NotImplementedError


@dataclasses.dataclass
class SimpleOrderPairSetBuilder(PairSetBuilder):
    bound_interval: datetime.timedelta = settings.SAME_MEAS_MAX_TIME_INTERVAL

    def in_same_pack(self, m1: Measurement, m2: Measurement) -> bool:
        # "до" "после" считаются только измерения разница которых больше 20 минут
        # и они находятся в разных днях
        return (
            m2.measurement_time - m1.measurement_time < self.bound_interval and
            m2.measurement_time.date() == m1.measurement_time.date()
        )

    def build_pairs(self, mss: typing.Iterable[Measurement]) -> PairSet:
        result = []
        packs: list[list[Measurement]] = []
        pack: list[Measurement] = []
        pack_last: typing.Optional[Measurement] = None

        # сгруппируем исследования на группы, разделенные по времени
        # одна группа - исследования в контексте SAME_MEAS_MAX_TIME_INTERVAL (от последнего исследования)
        # т.е. разница между группами всегда больше чем SAME_MEAS_MAX_TIME_INTERVAL
        for meas in mss:
            if pack_last is None:
                pack.append(meas)
                packs.append(pack)
                pack_last = meas
                continue

            if self.in_same_pack(pack_last, meas):
                pack.append(meas)
                pack_last = meas
                continue

            pack = [meas]
            pack_last = meas
            packs.append(pack)

        # проходимся по каждой группе и выбираем последнее измерение
        prev_pack: typing.Optional[list[Measurement]] = None
        for pack in packs:
            if prev_pack is None:
                prev_pack = pack
                continue

            prev = last(prev_pack)
            curr = last(pack)
            result.append(
                MeasurementPair(
                    date=curr.measurement_time.date(),
                    object=curr.object,
                    side=curr.side,
                    before=prev,
                    after=curr
                )
            )
            prev_pack = None

        return result
