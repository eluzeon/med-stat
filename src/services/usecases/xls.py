import os.path

from xlsxwriter import Workbook

import settings
from src.domain.models.measurement_pair import GroupPairSet
from src.xls.builder import WorkbookBuilder
from src.services.xls.pairset import AllGroupsPairSetSheet


def export_pairset_groups_to_excel(pairset: list[GroupPairSet], path: str) -> Workbook:
    filename = settings.EXCEL_FILE_NAME
    path = os.path.join(path, filename)

    return WorkbookBuilder()\
        .add_sheet(AllGroupsPairSetSheet(pairset)) \
        .build(path)
