import time
import typing

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src import logger
from src.app.ui.components.actionbar import QActionGrid
from src.app.ui.components.file_select import QFileSelect
from src.app.ui.components.line import QHLine
from src.app.ui.components.messages import message_error_occurred
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

        logger.ui.info(f"File selected: {path}")
        state.file_path = path
        self._file_path = path
        self.file_select.set_file_name(path)

        worker = LoadWorker(path)

        def on_finish() -> None:
            logger.ui.info("File loaded")
            self.action_bar.setDisabled(False)
            self.file_select.button.setDisabled(False)
            self.file_select.button.setText("Выбрать другой файл")

        def on_fail(e: Exception):
            logger.ui.warn(f"File loading failed {e}")
            message_error_occurred(self, e)

        worker.finished.connect(on_finish)
        worker.failed.connect(on_fail)
        thread = run_in_thread(worker, parent=self)
        # ???
        time.sleep(0.01)

        def on_start():
            logger.ui.info("File loading started")
            self.file_select.button.setDisabled(True)
            self.file_select.button.setText("Файл загружается...")
            self.action_bar.setDisabled(True)

        thread.started.connect(on_start)
