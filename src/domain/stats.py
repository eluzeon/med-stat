import dataclasses

from src.domain.models import Measurable


@dataclasses.dataclass
class Stat:
    after: Measurable
    before: Measurable
    diff: Measurable


@dataclasses.dataclass
class StatResult:
    avg: Stat
    stdev: Stat
    size: int = 0


@dataclasses.dataclass
class GroupStats:
    object: str
    side: str
    stats: StatResult
