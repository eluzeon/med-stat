import os
from traceback import print_exc

import settings
from src.app.cli.from_file import export_full_file
from src.app.cli.utils import resolve_path, make_path


def export_full_dir(dir_name: str) -> None:
    dir_name = resolve_path(dir_name)
    print(f"working dir is: {dir_name}")
    ok, fail = 0, 0
    for path, _, fnames in os.walk(dir_name):
        for fname in fnames:
            export_dir_path = make_path(settings.EXPORT_PATH, fname.rsplit('.', 1)[0])
            print(f"handling file {fname} in {export_dir_path}")
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
    export_full_dir(
        "@/exports/minis"
    )


"""
09.11.1974_Dmitry Zhukov.csv
27.03.2015_Alexandra Nicolaeva.csv
26.12.1993_Alla P.csv
"""
