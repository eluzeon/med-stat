from src import store
from src.services.usecases.graph import build_differ_and_save
from src.services.usecases.load import load_all_measurements
from src.services.usecases.stat import get_measurements_stats


def export_diff_graphs(to_path: str) -> None:
    """
    Выгружает diff- графики в папку :to_path:
    """
    stats = get_measurements_stats()
    build_differ_and_save(stats, to_path)


def load_file_content(file: str) -> None:
    """
    Загружает данные выбранного файла в память
    """
    store.clear()
    with open(file) as f:
        load_all_measurements(f.readlines())
