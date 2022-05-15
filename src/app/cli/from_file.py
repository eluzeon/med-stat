
"""
Делает тоже что и программа, только без UI
"""
import os.path
from traceback import print_exc

from src import store
from src.services import usecases


def _build_path(base: str, *paths: str) -> str:
    """ Создает папки если они не существуют """
    pth = base
    for path in paths:
        pth = os.path.join(pth, path)
        if not os.path.exists(pth):
            os.mkdir(pth)
    return pth


def export_full_file(from_path: str, to_path: str) -> None:
    result = usecases.load_file_content(from_path, raise_on_empty=True)

    mean_path = _build_path(to_path, "graphs", "mean")
    usecases.export_mean_graphs(mean_path)
    if result.ca_available:
        # получилось собрать пары "до" "после" - доступен сравнительный анализ
        diff_path = _build_path(to_path, "graphs", "diff")
        usecases.export_diff_graphs(diff_path)

        detail_path = _build_path(to_path, "graphs", "detail")
        usecases.export_details_graphs(detail_path)

    store.clear()


def export_full_dir(dir_name: str) -> None:
    print(f"working dir is {dir_name}")
    glob_path = "/Users/tamakarov/etc/med-stat/exports"
    ok, fail = 0, 0
    for path, _, fnames in os.walk(dir_name):
        for fname in fnames:
            print(f"handling file {fname}")
            export_dir_path = os.path.join(glob_path, "final", fname.rsplit('.', 1)[0])
            if not os.path.exists(export_dir_path):
                os.mkdir(export_dir_path)
            try:
                export_full_file(
                    os.path.join(path, fname),
                    export_dir_path
                )
            except Exception as e:
                print_exc()
                print(f"Failed to process {fname}: {e}")
                fail += 1
            else:
                ok += 1
    print(f"Done with OK: {ok}, FAILED: {fail}")


if __name__ == '__main__':
    export_full_dir('/Users/tamakarov/etc/med-stat/exports/minis')
