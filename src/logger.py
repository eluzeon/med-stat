import logging
import typing

import settings

_log_format = f"%(asctime)s::[%(levelname)s]::%(name)s: %(message)s"

default_formatter = logging.Formatter(_log_format)


def get_handlers() -> typing.Iterable[logging.Handler]:
    handlers = [logging.FileHandler(settings.LOGGING_FILE_PATH)]
    if settings.DEBUG:
        handlers.append(logging.StreamHandler())
    return handlers


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handlers = get_handlers()
    for handler in handlers:
        handler.setFormatter(default_formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger


ui = get_logger("UI")
service = get_logger("SERVICE")
worker = get_logger("WORKER")
app = get_logger("APP")
