import time
import typing

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.app.ui.components.actionbar import QActionGrid
from src.app.ui.components.file_select import QFileSelect
from src.app.ui.components.line import QHLine
from src.app.ui.state import state
from src.app.ui.workers.load_worker import LoadWorker
from src.app.ui.workers.threads import run_in_thread


class QCompositeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._file_path = None

        layout = QVBoxLayout()
        self.file_select = QFileSelect()
        self.file_select.on_file_selected.connect(self.on_file_selected)
        self.action_bar = QActionGrid()
        self.action_bar.setDisabled(True)

        layout.addWidget(self.file_select)
        layout.addWidget(QHLine())
        layout.addWidget(self.action_bar)
        self.setLayout(layout)

    def on_file_selected(self, path: typing.Optional[str]) -> None:
        if not path:
            return

        state.file_path = path
        self._file_path = path
        self.file_select.set_file_name(path)

        worker = LoadWorker(path)

        def on_finish() -> None:
            self.action_bar.setDisabled(False)
            self.file_select.button.setDisabled(False)
            self.file_select.button.setText("Выбрать другой файл")

        worker.finished.connect(on_finish)
        run_in_thread(worker, parent=self)
        # ???
        time.sleep(0.01)
        self.file_select.button.setDisabled(True)
        self.file_select.button.setText("Файл загружается...")
