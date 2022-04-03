from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal

from src.app.ui.workers.threads import Worker
from src.services.usecases import load_file_content


class LoadWorker(Worker):
    finished: pyqtBoundSignal = pyqtSignal()

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> None:
        load_file_content(self.path, raise_on_empty=True)
