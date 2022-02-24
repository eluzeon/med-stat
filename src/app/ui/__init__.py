import sys

from PyQt6.QtWidgets import QApplication
from src.app.ui.main import MainWindow


def start_gui():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
