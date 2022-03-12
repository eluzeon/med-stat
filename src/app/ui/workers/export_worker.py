from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal

from src.app.ui.workers.threads import Worker
from src.services.usecases import export_diff_graphs, export_pairset_to_excel


class ExportGraphWorker(Worker):
    finished: pyqtBoundSignal = pyqtSignal()

    def __init__(self, dir_path: str):
        super().__init__()
        self.dir_path = dir_path

    def run(self) -> None:
        export_diff_graphs(self.dir_path)
        self.finished.emit()


class ExportExcelWorker(Worker):
    finished: pyqtBoundSignal = pyqtSignal()

    def __init__(self, dir_path: str):
        super().__init__()
        self.dir_path = dir_path

    def run(self) -> None:
        export_pairset_to_excel(self.dir_path)
        self.finished.emit()
