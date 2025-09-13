import logging
import datetime
import logging.config
import functools
import os

LOGS_DIR="logs"
os.makedirs(LOGS_DIR, exist_ok=True)

class AienergyFormatter(logging.Formatter):
    def format(self, record):
        record.reference_id = debug_data["referenceId"]
        self.use_colors = True 
        return super().format(record)
    
DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": AienergyFormatter,
            "format": "%(asctime)s.%(msecs)03d %(levelname)s %(reference_id)s: %(message)s",
            # "format": "%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "uvicorn": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": f"./{LOGS_DIR}/log_info_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log",
            "mode": "a",
            "encoding": "utf-8",
            "delay": True,
        },
    },
    "loggers": {
        "local": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
        "local.file": {"handlers": ["file"], "level": "INFO", "propagate": False},
        "local.console": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn": {"handlers": ["uvicorn"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["uvicorn"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["uvicorn"], "level": "INFO", "propagate": False},
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

def init_local_logging() -> None:
    """
    Initializes the local logging configuration.
    """
    logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)

def get_logger() -> logging.Logger:
    """
    Returns the logger.
    If running under uvicorn, it will return the uvicorn logger.
    Otherwise, it will return the logger for the current module.
    """
    logger = logging.getLogger(os.environ.get("AIENERGY_LOGGER", "uvicorn.error"))
    if not logger.hasHandlers():
        # logger = logging.getLogger(__name__)
        logger = logging.getLogger("local")
    return logger

def add_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # global logger
        logger = get_logger()
        try:
            logger.info(f"{func.__name__} started")
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} finished")
            return result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e

    return wrapper


default_debug_data = {
    "referenceId": "NO_REF",
    "location": "DEBUG_NOT_INITIALISED",
    "systemType": "DEBUG_NOT_INITIALISED",
    "userAccountType": "DEBUG_NOT_INITIALISED", 
    "yearlyConsumption": "DEBUG_NOT_INITIALISED",
    "optimizationType": "DEBUG_NOT_INITIALISED",
}
debug_data = default_debug_data

@staticmethod
def set_debug_data(input_data: dict):
    """
    Set debug data from input data.
    """
    global debug_data
    debug_data = {key: input_data[key] for key in input_data.keys() & default_debug_data.keys()} 
    debug_data = default_debug_data | debug_data

@staticmethod
def dump_debug(label: str = None):
    """
    Dump debug data to log.
    """
    logger = get_logger()
    message = f"logger DEBUG DATA:\n{debug_data}"
    if label:
        message = f"[{label}] {message}"
    logger.info(message)

init_local_logging()