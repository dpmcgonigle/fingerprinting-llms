import logging
from logging import handlers as handlers


def setup_logger(
    log_file: str | None = None,
    log_level: int | None = logging.INFO,
    syslog: bool | None = False,
) -> None:
    msg_format = (
        "[%(asctime)s] p%(process)s {%(filename)s "
        "%(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # always add console logging
    log_handlers: list[logging.Handler] = [logging.StreamHandler()]

    if log_file:
        log_handlers.append(_file_handler(log_file))

    if syslog:
        log_handlers.append(_syslog_handler())

    logging.basicConfig(
        format=msg_format,
        datefmt=date_format,
        level=log_level,
        handlers=log_handlers,
    )


def _file_handler(log_file: str) -> logging.Handler:
    return handlers.RotatingFileHandler(log_file, maxBytes=25600000, backupCount=10)


def _syslog_handler() -> logging.Handler:
    raise NotImplementedError()
