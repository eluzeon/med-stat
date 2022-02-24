import os.path
import typing

from PyQt6.QtCore import Qt, pyqtSignal, pyqtBoundSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from PyQt6.uic.properties import QtGui


class QFileSelect(QWidget):
    DEFAULT_LABEL = "Файл не выбран"
    on_file_selected: pyqtBoundSignal = pyqtSignal(str)

    def __init__(self):
        super(QFileSelect, self).__init__()
        self._file_name: typing.Optional[str] = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self._label = QLabel(text=self._file_name or self.DEFAULT_LABEL)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Открыть файл")
        self.button.clicked.connect(self.open_file_browser)
        self.button.setMaximumWidth(200)

        layout.addWidget(self._label)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def open_file_browser(self):
        file, _ = QFileDialog.getOpenFileName(self, filter="CSV files (*.csv)")
        self.on_file_selected.emit(file)

    def _path_as_title(self, path: typing.Optional[str]) -> str:
        if not path:
            return ""
        parts = path.split(os.path.sep)
        return parts[-1] if parts else ""

    def set_file_name(self, name: str) -> None:
        self.button.setText("Выбрать другой файл")
        self._file_name = name
        self._label.setText(self._path_as_title(self._file_name))

    def clean(self) -> None:
        self._file_name = None
        self.button.setText("Открыть файл")
        self._label.setText(self.DEFAULT_LABEL)
