import datetime
import logging
import os

class Logger:

    default_debug_data = {
        "referenceId": "DEBUG_NOT_INITIALISED",
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
        Logger.debug_data = {key: input_data[key] for key in input_data.keys() & Logger.default_debug_data.keys()} 
        Logger.debug_data = Logger.default_debug_data | Logger.debug_data

    @staticmethod
    def dump_debug(label: str = None):
        """
        Dump debug data to log.
        """
        message = f"Logger DEBUG DATA:\n{Logger.debug_data}"
        if label:
            message = f"[{label}] {message}"
        Logger.info(message)

    @staticmethod
    def info(message: str):
        """
        Log a message with severity 'INFO' using logging.info(). Adds debug data to the message.
        """
        message = f"[{Logger.debug_data['referenceId']}] {message}"
        logging.info(message)

    @staticmethod
    def error(message: str):
        """
        Log a message with severity 'ERROR' using logging.info(). Adds debug data to the message.
        """
        message = f"[{Logger.debug_data['referenceId']}] {message}"
        logging.error(message)


    def __init__(self, path: str) -> None:
        """
        Initializes the Logger object.
        """
        self.path = path
        self.log_filename = self._generate_log_filename()
        self._create_log_folder()
        self._setup_logger()

    def _generate_log_filename(self) -> str:
        """
        Generates the log file name with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        return f"{self.path}/log_info_{timestamp}.log"

    def _create_log_folder(self) -> None:
        """
        Creates the log folder if it doesn't exist.
        """
        os.makedirs(self.path, exist_ok=True)

    def _setup_logger(self) -> None:
        """
        Configures the logging settings for the logger.
        """
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(filename)-5s %(levelname)-8s %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            filename=self.log_filename
        )
