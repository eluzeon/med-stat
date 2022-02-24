from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout

from src.app.ui.workers.export_worker import ExportWorker
from src.app.ui.workers.threads import run_in_thread


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


class QActionExportGraphs(QActionButton):
    def __init__(self):
        super().__init__(
            "Выгрузить графики",
            "Создает и выгружает графики в указанную папку"
        )

    def handle_on_click(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        self._run_export_thread(dir_path)

    def _run_export_thread(self, dir_path: str):
        worker = ExportWorker(dir_path)

        run_in_thread(worker, parent=self)
        self.button.setEnabled(False)
        self.button.setText("Подождите...")

        def on_finish():
            self.button.setEnabled(True)
            self.button.setText(self.title)

        worker.finished.connect(on_finish)


class QActionExportExcel(QActionButton):
    def __init__(self):
        super(QActionExportExcel, self).__init__(
            "Выгрузить в EXCEL",
            "Выгрузка данных файла в EXCEL с подсчитанными данными"
        )
