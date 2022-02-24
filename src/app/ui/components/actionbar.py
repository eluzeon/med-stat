from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from src.app.ui.components.action_button import QActionButton, QActionExportGraphs, QActionExportExcel


class QActionGrid(QWidget):
    DEFAULT_ACTION = "Выберите действие"

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QGridLayout()

        buttons = self._buttons()
        for i, button in enumerate(buttons):
            layout.addWidget(button, i // 3 + 1, i % 3 + 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def _buttons(self) -> list[QActionButton]:
        return [
            QActionExportGraphs(),
            QActionExportExcel(),
        ]

