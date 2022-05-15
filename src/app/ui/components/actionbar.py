from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from src.app.ui.components.action_button import QActionButton, QActionExportGraphs, QActionExportExcel, \
    QActionExportDetailGraphs, QActionMeanGraph


class QActionGrid(QWidget):
    def __init__(self, buttons: list[QActionButton]):
        super().__init__()
        self._buttons = buttons
        self.setMinimumHeight(140)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QGridLayout()

        for i, button in enumerate(self._buttons):
            layout.addWidget(button, i // 3 + 1, i % 3 + 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    @classmethod
    def compare_analysis(cls):
        return cls(
            [
                QActionExportGraphs(),
                QActionExportExcel(),
                QActionExportDetailGraphs()
            ],
        )

    @classmethod
    def single_analysis(cls):
        return cls([QActionMeanGraph()])
