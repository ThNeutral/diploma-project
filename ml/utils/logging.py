import logging
import sys
from typing import Any


def _setup_logger() -> logging.Logger:
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    logger.addHandler(handler)
    logger.propagate = False
    return logger


_LOGGER = _setup_logger()


def debug(msg: Any, *args: Any, **kwargs: Any) -> None:
    _LOGGER.debug(msg, *args, **kwargs)


def info(msg: Any, *args: Any, **kwargs: Any) -> None:
    _LOGGER.info(msg, *args, **kwargs)


def warning(msg: Any, *args: Any, **kwargs: Any) -> None:
    _LOGGER.warning(msg, *args, **kwargs)


def error(msg: Any, *args: Any, **kwargs: Any) -> None:
    _LOGGER.error(msg, *args, **kwargs)


def critical(msg: Any, *args: Any, **kwargs: Any) -> None:
    _LOGGER.critical(msg, *args, **kwargs)


def exception(msg: Any, *args: Any, **kwargs: Any) -> None:
    _LOGGER.exception(msg, *args, **kwargs)