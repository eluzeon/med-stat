import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout

from src import logger
from src.app.ui.components.messages import message_error_occurred
from src.app.ui.workers.export_worker import ExportGraphWorker, ExportExcelWorker, ExportDetailGraphsWorker
from src.app.ui.workers.threads import run_in_thread, Worker


class QActionButton(QWidget):
    def __init__(self, label: str, description: str):
        super().__init__()
        self.title = label
        self.button = QPushButton(text=label)
        self.label = QLabel(text=description)
        self.label.setMaximumWidth(150)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button.clicked.connect(self.handle_on_click)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def handle_on_click(self):
        pass


class WorkerActionButton(QActionButton):
    def get_worker(self, *args, **kwargs) -> Worker:
        raise NotImplementedError()

    def handle_on_click(self):
        logger.ui.info(f"Clicked on ActionButton: {self.__class__.__name__}")
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self._run_export_thread(dir_path)

    def _run_export_thread(self, dir_path: str):
        worker = self.get_worker(dir_path)

        logger.ui.info(f"Starting worker: {worker.__class__.__name__}")
        run_in_thread(worker, parent=self)
        # todo: не знаю почему, но так работает,
        #  а без этого не всегда
        time.sleep(0.01)
        self.button.setEnabled(False)
        self.button.setText("Подождите...")

        def on_finish():
            logger.ui.info(f"ActionButton {worker.__class__.__name__} finished")
            self.button.setEnabled(True)
            self.button.setText(self.title)

        def on_failed(e: Exception):
            logger.ui.exception(f"ActionButton {worker.__class__.__name__} failed with exception {e}")
            message_error_occurred(self, e)
            on_finish()

        worker.finished.connect(on_finish)
        worker.failed.connect(on_failed)


class QActionExportGraphs(WorkerActionButton):
    def __init__(self):
        super().__init__(
            "Diff-графики",
            "Создает и выгружает графики в указанную папку"
        )

    def get_worker(self, *args, **kwargs) -> Worker:
        return ExportGraphWorker(*args, **kwargs)


class QActionExportDetailGraphs(WorkerActionButton):
    def __init__(self):
        super().__init__(
            "Details-грифики",
            "Выгружает детализированные графики"
        )

    def get_worker(self, *args, **kwargs) -> Worker:
        return ExportDetailGraphsWorker(*args, **kwargs)


class QActionExportExcel(WorkerActionButton):
    def __init__(self):
        super(QActionExportExcel, self).__init__(
            "Выгрузить в EXCEL",
            "Выгрузка данных файла в EXCEL с подсчитанными данными"
        )

    def get_worker(self, *args, **kwargs) -> Worker:
        return ExportExcelWorker(*args, **kwargs)
