from PyQt6.QtWidgets import QMainWindow

from src.app.ui.components.composite_widget import QCompositeWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        w = QCompositeWidget()
        self.setCentralWidget(w)
