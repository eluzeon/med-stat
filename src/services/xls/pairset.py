import dataclasses

from marshmallow import EXCLUDE
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

import settings
from src.domain.models import Measurable
from src.domain.models.measurement_pair import MeasurementPairSchema, MeasurementPair, GroupPairSet
from src.services.stat.pair import diff
from src.services.stat.pairset import calc_stats
from src.xls import Sheet, Field, FieldSet, ValueSet, Value
from src.xls.headers import default_write_fieldset
from src.xls.values import ValueOptions


def attr_sub_fields() -> list[Field]:
    return [
        Field('до'),
        Field('sem'),
        Field('после'),
        Field('sem'),
        Field('измен'),
        Field('sem'),
    ]


FIELDS = FieldSet(
    Field("Measurement Time"),
    Field("Object"),
    Field("Side"),
    Field("Frequency", attr_sub_fields()),
    Field("Stiffness", attr_sub_fields()),
    Field("Decrement", attr_sub_fields()),
    Field("Relaxation", attr_sub_fields()),
    Field("Creep", attr_sub_fields())
)


@dataclasses.dataclass
class AllGroupsPairSetSheet(Sheet):
    data: list[GroupPairSet]
    colors: list[str] = dataclasses.field(default_factory=lambda: settings.EXCEL_DATA_COLORS)

    @property
    def dumped(self):
        schema = MeasurementPairSchema(unknown=EXCLUDE)
        return schema.dump(self.data, many=True)

    def __add_headers(self, sh: Worksheet, fields: FieldSet) -> None:
        default_write_fieldset(fields, sh)

    def _add_for_attrs(self, vs: ValueSet, pair: MeasurementPair, pair_diff: Measurable, row_i: int):
        fields = dataclasses.fields(Measurable)
        for fmt, field in zip(self._bg_formats, fields):
            attr = field.name
            opt = ValueOptions(fmt)
            vs.add_value(row_i, getattr(pair.before, attr), options=opt)
            vs.add_value(row_i, getattr(pair.before, f"{attr}_error"), options=opt)
            vs.add_value(row_i, getattr(pair.after, attr), options=opt)
            vs.add_value(row_i, getattr(pair.after, f"{attr}_error"), options=opt)
            vs.add_value(row_i, getattr(pair_diff, attr), options=opt)
            vs.add_value(row_i, "", options=opt)

    def _add_stats_result(self, group: GroupPairSet, vs: ValueSet, row_i: int):
        stats = calc_stats(group.pairset)
        fields = dataclasses.fields(Measurable)
        for i, field in enumerate(fields):
            attr = field.name
            option = ValueOptions(self._bg_formats[i])
            vs.add(Value(row_i, getattr(stats.avg.before, attr), col=(i * 6) + 3, options=option))
            vs.add(Value(row_i, getattr(stats.stdev.before, attr), col=(i * 6) + 4, options=option))
            vs.add(Value(row_i, getattr(stats.avg.after, attr), col=(i * 6) + 5, options=option))
            vs.add(Value(row_i, getattr(stats.stdev.after, attr), col=(i * 6) + 6, options=option))
            vs.add(Value(row_i, getattr(stats.avg.diff, attr), col=(i * 6) + 7, options=option))
            vs.add(Value(row_i, getattr(stats.stdev.diff, attr), col=(i * 6) + 8, options=option))

        vs.next_row()

    def _handle_single_group(self, group: GroupPairSet, vs: ValueSet, start: int) -> int:
        row_i = 0
        for row_i, row in enumerate(group.pairset, start=start):
            pair_diff = diff(row)
            base = row.before
            vs.add_value(row_i, base.measurement_time)
            vs.add_value(row_i, row.object)
            vs.add_value(row_i, row.side)

            self._add_for_attrs(vs, row, pair_diff, row_i)

            vs.next_row()

        row_i += 2
        self._add_stats_result(group, vs, row_i)
        return row_i + 1

    def add(self, wb: Workbook) -> Worksheet:
        sh = wb.add_worksheet("All groups")
        self.__add_headers(sh, FIELDS)
        vs = ValueSet()

        self._bg_formats = [
            wb.add_format({"bg_color": col, "font_size": 16})
            for col in self.colors
        ]

        row_i = 0
        for group in self.data:
            row_i = self._handle_single_group(group, vs, row_i + 2)

        vs.write(sh)
        return sh
