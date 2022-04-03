from src.app.ui import start_gui
from src import logger


def on_startup() -> None:
    pass


def start_app() -> None:
    try:
        logger.app.info("Starting up app")
        on_startup()
        logger.app.info("Starting up GUI")
        start_gui()
    except Exception as e:
        logger.app.exception("Unhandled exception", exc_info=e)
