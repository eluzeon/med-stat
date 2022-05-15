from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal

from src.app.ui.workers.threads import Worker
from src.domain.load_result import LoadResult
from src.services.usecases import load_file_content


class LoadWorker(Worker):
    finished: pyqtBoundSignal = pyqtSignal(LoadResult)

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> LoadResult:
        return load_file_content(self.path, raise_on_empty=True)
