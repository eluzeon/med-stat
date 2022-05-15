from src import store
from src.domain.exceptions import PairSetBuilderError
from src.domain.load_result import LoadResult
from src.services.dao.measurements import get_measurements
from src.services.grouper import get_object_side_groups
from src.services.usecases.graph import build_differ_and_save, build_detail_graphs_and_save, build_mean_graphs_and_save
from src.services.usecases.load import load_all_measurements, get_all_groups
from src.services.usecases.stat import get_measurements_stats
from src.services.usecases.xls import export_pairset_groups_to_excel


def export_diff_graphs(to_path: str) -> None:
    """
    Выгружает diff- графики в папку :to_path:
    """
    stats = get_measurements_stats()
    build_differ_and_save(stats, to_path)


def export_details_graphs(path: str) -> None:
    groups = get_all_groups()
    build_detail_graphs_and_save(groups, path)


def export_mean_graphs(path: str) -> None:
    mss = get_measurements()
    groups = get_object_side_groups(mss)
    build_mean_graphs_and_save(groups, path)


def export_pairset_to_excel(path: str) -> None:
    """
    Выгружает все данные в EXCEL
    """
    groups = get_all_groups()
    export_pairset_groups_to_excel(groups, path)


def load_file_content(file: str, raise_on_empty: bool = False) -> LoadResult:
    """
    Загружает данные выбранного файла в память
    """
    store.clear()
    with open(file) as f:
        mss = load_all_measurements(f.readlines())
        if not mss and raise_on_empty:
            raise ValueError(
                "Выбранный файл пуст или не удалось обработать его содержание"
            )
        # build groups, to get error immediately
        try:
            get_all_groups()
            return LoadResult(True)
        except PairSetBuilderError as e:
            message = "Не удалось группировать данные для сравнительного анализа. " \
                      "Сравнительный анализ недоступен. Если Вы хотите сделать сравнительный анализ, " \
                      "проверьте правильность файла: необходимы исследования с разницей более 20 минут, " \
                      f"которые будут считаться за \"до\" и \"после\". Ошибка: {e.message}"
            return LoadResult(False, message)
