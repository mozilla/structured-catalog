import sys

from mozlog.structured.formatters import MachFormatter
from mozlog.structured.structuredlog import (
    StructuredLogger,
    get_default_logger,
    set_default_logger,
)
from mozlog.structured.handlers import (
    StreamHandler,
    LogLevelFilter,
)

def create_logger(name='catalog', stream=None, level='debug'):
    stream = stream or sys.stdout
    logger = StructuredLogger(name)
    formatter = LogLevelFilter(MachFormatter(), level)
    logger.add_handler(StreamHandler(stream, formatter))
    set_default_logger(logger)
    return logger

def get_logger(*args, **kwargs):
    return get_default_logger() or create_logger(*args, **kwargs)

