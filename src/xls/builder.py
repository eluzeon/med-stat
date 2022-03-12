import dataclasses

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet


class Sheet:
    def add(self, wb: Workbook) -> Worksheet:
        raise NotImplementedError()


@dataclasses.dataclass
class WorkbookBuilder:
    sheets: list[Sheet] = dataclasses.field(default_factory=list)

    def add_sheet(self, sheet: Sheet) -> 'WorkbookBuilder':
        self.sheets.append(sheet)
        return self

    def build(self, path: str) -> Workbook:
        wb = Workbook(path)
        wb.formats[0].set_font_size(16)
        for sh in self.sheets:
            sh.add(wb)
        wb.close()
        return wb
