import dataclasses
import datetime


@dataclasses.dataclass
class DateTimeRange:
    date_from: datetime.datetime
    date_to: datetime.datetime

    def __post_init__(self) -> None:
        if self.date_to < self.date_from:
            raise ValueError(f"{self.date_to=} is less than {self.date_from=} parameter")

    def __contains__(self, item: datetime.datetime) -> bool:
        return (
            self.date_from <= item < self.date_to
        )
