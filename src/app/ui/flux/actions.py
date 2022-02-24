import dataclasses
import typing


@dataclasses.dataclass
class Action:
    name: str
    payload: typing.Any


class SelectFileAction(Action):
    def __init__(self, path: str):
        super().__init__(
            name="[File] Select",
            payload={"path": path}
        )
