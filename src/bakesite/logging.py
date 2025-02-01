import logging
import logging.config

logging_config = {
    "version": 1,
    "formatters": {
        "console": {"format": "%(asctime)s: %(levelname)s: [%(module)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "console",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Change to stdout
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
logging.config.dictConfig(logging_config)
