from src import store
from src.services.usecases.graph import build_differ_and_save
from src.services.usecases.load import load_all_measurements, get_all_groups
from src.services.usecases.stat import get_measurements_stats
from src.services.usecases.xls import export_pairset_groups_to_excel


def export_diff_graphs(to_path: str) -> None:
    """
    Выгружает diff- графики в папку :to_path:
    """
    stats = get_measurements_stats()
    build_differ_and_save(stats, to_path)


def export_pairset_to_excel(path: str) -> None:
    """
    Выгружает все данные в EXCEL
    """
    pairset = get_all_groups()
    export_pairset_groups_to_excel(pairset, path)


def load_file_content(file: str) -> None:
    """
    Загружает данные выбранного файла в память
    """
    store.clear()
    with open(file) as f:
        load_all_measurements(f.readlines())
