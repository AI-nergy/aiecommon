import datetime
import logging
import os

class Logger:
    """
    A class for generating and configuring loggers

    ...

    Methods
    -------
    generate_logger()
        Generates a logger object
    """
    def __init__(self, path) -> None:
        self.path = path
        # Create folder in case it does not exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)



    def generate_logger(self):
        """
        Generates a logger object

        Returns
        -------
        logger object
            An instance of the configured logger
        """
        self._setup_logger()

        return logging.getLogger(__name__)

    def _setup_logger(self):
        """
        Configures the logging settings for the logger
        """
        # configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(filename)-5s %(levelname)-8s %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            filemode="a",
            filename=self._get_log_filename()
        )

    def _get_log_filename(self):
        """
        Creates a log file name based on the current time
        Returns
        -------
        str
            log filename in the format 'log_info_{ref_id}_{current_time}.log'
        """
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        return f"{self.path}/log_info_{current_time}.log"
