import dataclasses
import typing


@dataclasses.dataclass
class LoadResult:
    # is composition analysis available?
    ca_available: bool
    ca_error: typing.Optional[str] = None
