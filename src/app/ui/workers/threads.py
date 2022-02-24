import typing

from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtBoundSignal


class Worker(QObject):
    finished: pyqtBoundSignal = pyqtSignal()

    def run(self) -> None:
        raise NotImplementedError


def run_in_thread(worker: Worker, parent: typing.Optional[QObject] = None) -> QThread:
    thread = QThread(parent=parent)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    thread.start()

    return thread
