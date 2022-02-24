import csv
import typing

from marshmallow import EXCLUDE

import settings
from src.domain.models import TapSchema, Tap
from src.utils import find

_schema = TapSchema(unknown=EXCLUDE)


def parse_tap_row(row: dict[str, typing.AnyStr]) -> Tap:
    kws = {}
    for field, model_field in settings.CSV_INPUT_FIELDS_MAPPING.items():
        if isinstance(field, tuple):
            field = find(lambda x: x in row, field)
        kws[model_field] = row.get(field, None) if field else None
    return _schema.load(kws)


def load_taps(itr: typing.Iterable[str]) -> list[Tap]:
    reader = csv.DictReader(
        itr,
        delimiter=settings.CSV_DELIMITER
    )
    return [
        parse_tap_row(row)
        for i, row in enumerate(reader)
    ]
