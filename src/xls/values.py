import dataclasses
import typing

from marshmallow import ValidationError, Schema
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet


@dataclasses.dataclass
class ValueOptions:
    format: Format


@dataclasses.dataclass
class Value:
    index: int
    value: typing.Any
    col: typing.Optional[int] = None  # None means auto
    options: typing.Optional[ValueOptions] = None


class Split(Value):
    def __init__(self):
        pass


@dataclasses.dataclass
class ValueSet:
    values: list[Value] = dataclasses.field(default_factory=list)

    def _dump_value(self, val: typing.Any, schema: typing.Optional[Schema] = None):
        if schema:
            return schema.dump(val)
        ma_filed = Schema.TYPE_MAPPING.get(type(val))
        if ma_filed:
            try:
                return ma_filed()._serialize(val, "", None)
            except ValidationError as e:
                print(type(val))
                print(val)
                print(ma_filed)
                raise ValueError(f"cannot dump value '{val}': dump error") from e
        raise ValueError(f"cannot dump value '{val}': field not found")

    def write(self, sheet: Worksheet, schema: typing.Optional[Schema] = None) -> typing.Any:
        col = 0
        for val in self.values:
            if isinstance(val, Split):
                col = 0
                continue
            sheet.write(
                val.index,
                col if val.col is None else val.col,
                self._dump_value(val.value, schema),
                val.options.format if val.options else None
            )
            col += 1

    def add(self, value: Value):
        self.values.append(value)

    def add_value(self, index: int, value: typing.Any, col: typing.Optional[int] = None,
                  options: typing.Optional[ValueOptions] = None):
        self.add(Value(index, value, col, options))

    def next_row(self):
        self.add(Split())
