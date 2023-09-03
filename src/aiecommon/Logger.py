import datetime
import logging
import os

class Logger:
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
