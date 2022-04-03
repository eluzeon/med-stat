import sys

from PyQt6.QtWidgets import QApplication

from src import logger
from src.app.ui.main import MainWindow


def start_gui():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    logger.app.info("Shutting down app")
    sys.exit(app.exec())
