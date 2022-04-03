import typing

from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtBoundSignal

from src import logger


class Worker(QObject):
    finished: pyqtBoundSignal = pyqtSignal()
    failed: pyqtBoundSignal = pyqtSignal(Exception)

    def run(self) -> None:
        raise NotImplementedError

    def exec(self) -> None:
        try:
            logger.worker.info(f"Worker {self.__class__.__name__} started")
            retval = self.run()
            logger.worker.info(f"Worker {self.__class__.__name__} run() finished with {str(retval)}")
            if retval:
                self.finished.emit(retval)
            else:
                self.finished.emit()
        except Exception as e:
            logger.worker.exception(f"Worker {self.__class__.__name__} failed with exception {e}")
            self.failed.emit(e)


def run_in_thread(worker: Worker, parent: typing.Optional[QObject] = None) -> QThread:
    thread = QThread(parent=parent)
    worker.moveToThread(thread)
    thread.started.connect(worker.exec)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    thread.start()

    return thread
