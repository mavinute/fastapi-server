import logging
from logging.config import dictConfig

LOG_FORMAT = "%(levelname)s | %(asctime)s | %(name)s | %(message)s"

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": LOG_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    },
}

def setup_logging():
    dictConfig(LOG_CONFIG)
