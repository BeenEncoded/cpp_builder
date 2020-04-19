import logging, os

from data import Configuration

CONFIG = Configuration()
LOG_LEVEL = {
    "critical": logging.CRITICAL,
    "error":    logging.ERROR,
    "warning":  logging.WARNING,
    "info":     logging.INFO,
    "debug":    logging.DEBUG,
    "notset":   logging.NOTSET}[CONFIG['DEFAULT']['loglevel']]

LOGFILE = Configuration.program_home + os.path.sep + "builder.log"