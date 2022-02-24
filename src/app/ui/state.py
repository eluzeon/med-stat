import dataclasses
import typing


@dataclasses.dataclass
class AppState:
    file_path: typing.Optional[str] = None


state = AppState()
