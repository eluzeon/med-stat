import time
import typing

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src import logger
from src.app.ui.components.actionbar import QActionGrid
from src.app.ui.components.file_select import QFileSelect
from src.app.ui.components.line import QHLine
from src.app.ui.components.messages import message_error_occurred, message_warning
from src.app.ui.state import state
from src.app.ui.workers.load_worker import LoadWorker
from src.app.ui.workers.threads import run_in_thread
from src.domain.load_result import LoadResult


class QCompositeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._file_path = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.file_select = QFileSelect()
        self.file_select.on_file_selected.connect(self.on_file_selected)
        self.action_bar = QActionGrid.compare_analysis()
        self.action_bar.setDisabled(True)

        self.action_bar_s = QActionGrid.single_analysis()
        self.action_bar_s.setDisabled(True)

        layout.addWidget(self.file_select)
        layout.addWidget(QHLine())
        layout.addWidget(self.action_bar_s)
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

        def on_finish(result: LoadResult) -> None:
            logger.ui.info("File loaded")
            self.action_bar_s.setDisabled(False)
            self.file_select.button.setDisabled(False)
            self.file_select.button.setText("Выбрать другой файл")
            if result.ca_available:
                self.action_bar.setDisabled(False)
            else:
                self.action_bar.setDisabled(True)
                message_warning(self, result.ca_error)

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
            self.action_bar_s.setDisabled(True)

        thread.started.connect(on_start)
