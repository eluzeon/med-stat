from PyQt6.QtCore import pyqtSignal

from src.app.ui.workers.threads import Worker
from src.services.usecases import load_file_content


class LoadWorker(Worker):
    finished = pyqtSignal()

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> None:
        print("WORKING")
        load_file_content(self.path)
        self.finished.emit()
