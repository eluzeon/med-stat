import dataclasses
import typing

from xlsxwriter.worksheet import Worksheet


@dataclasses.dataclass
class Field:
    name: str
    sub_fields: list['Field'] = dataclasses.field(default_factory=list)


class FieldSet:
    def __init__(self, *fields: Field):
        self.fields = fields

    def __flatten_fields(self, fields: typing.Iterable[Field]) -> typing.Iterable[Field]:
        for f in fields:
            yield f
            if f.sub_fields:
                yield from self.__flatten_fields(f.sub_fields)

    def _get_indexed_fields(self) -> typing.Generator[tuple[int, Field], None, None]:
        for i, field in enumerate(self.__flatten_fields(self.fields)):
            yield i, field

    def flatten_iter(self):
        return self._get_indexed_fields()

    def __iter__(self):
        return iter(self.fields)


def default_write_fieldset(fields: typing.Iterable[Field], sh: Worksheet, start: int = 0, deep: int = 0):
    """
    Записывает переданные поля в следующем виде
    | field1     |           | field2 | field3    |
    | sub_field1 | subfield2 |        | subfield1 |
    """
    i = start
    for field in fields:
        sh.write(deep, i, field.name)
        if field.sub_fields:
            default_write_fieldset(field.sub_fields, sh, start=i, deep=deep + 1)
            i += len(field.sub_fields) - 1
        i += 1
