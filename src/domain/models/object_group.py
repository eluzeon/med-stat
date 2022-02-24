import dataclasses

from src.domain.models import Measurement


@dataclasses.dataclass
class ObjectGroup:
    object: str
    measurements: list[Measurement]
