from src.app.ui.workers.threads import Worker
from src.services import usecases as uc


class ExportGraphWorker(Worker):
    def __init__(self, dir_path: str):
        super().__init__()
        self.dir_path = dir_path

    def run(self) -> None:
        uc.export_diff_graphs(self.dir_path)


class ExportTimeCompareGraphsWorker(Worker):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> None:
        uc.export_time_compare_graphs(self.path)


class ExportMeanGraphWorker(Worker):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> None:
        uc.export_mean_graphs(self.path)


class ExportExcelWorker(Worker):
    def __init__(self, dir_path: str):
        super().__init__()
        self.dir_path = dir_path

    def run(self) -> None:
        uc.export_pairset_to_excel(self.dir_path)


class ExportDetailGraphWorker(Worker):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> None:
        return uc.export_detailed_measurement_graphs(self.path)
