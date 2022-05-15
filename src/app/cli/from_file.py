
"""
Делает тоже что и программа, только без UI
"""
from src import store
from src.app.cli.utils import make_path
from src.services import usecases


def export_full_file(from_path: str, to_path: str) -> None:
    result = usecases.load_file_content(from_path, raise_on_empty=True)

    mean_path = make_path(to_path, "graphs", "mean")
    usecases.export_mean_graphs(mean_path)

    if result.ca_available:
        # получилось собрать пары "до" "после" - доступен сравнительный анализ
        diff_path = make_path(to_path, "graphs", "diff")
        usecases.export_diff_graphs(diff_path)

        detail_path = make_path(to_path, "graphs", "detail")
        usecases.export_details_graphs(detail_path)

        xls_path = make_path(to_path, "xls")
        usecases.export_pairset_to_excel(xls_path)
    store.clear()

