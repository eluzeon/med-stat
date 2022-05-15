import traceback
import typing

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox


def _default_builder(parent: QObject, title: str, message: str) -> QMessageBox:
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(message)
    return dlg


def message_dir_not_found(parent: QObject):
    _default_builder(parent, "Внимание", "Такого пути не существует").exec()


def message_error_occurred(parent: QObject, err: typing.Union[Exception, str]):
    _default_builder(parent, "Ошибка", str(err)).exec()


def message_warning(parent: QObject, warn: str):
    _default_builder(parent, "Внимание", warn).exec()
