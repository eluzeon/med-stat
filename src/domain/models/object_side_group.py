import dataclasses

from src.domain.models.object_group import ObjectGroup


@dataclasses.dataclass
class ObjectSideGroup(ObjectGroup):
    side: str
