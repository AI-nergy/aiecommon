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

    LOG_FOLDER = "./logs"

    @staticmethod
    def generate_logger():
        """
        Generates a logger object

        Returns
        -------
        logger object
            An instance of the configured logger
        """

        Logger._generate_logger_folder_if_not_exists()
        Logger._setup_logger()

        return logging.getLogger(__name__)
 
    @staticmethod
    def _setup_logger():
        """
        Configures the logging settings for the logger
        """
        # configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(filename)-5s %(levelname)-8s %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            filemode="a",
            filename=Logger._get_log_filename()
        )

    @staticmethod
    def _get_log_filename():
        """
        Creates a log file name based on the current time
        Returns
        -------
        str
            log filename in the format 'log_info_{ref_id}_{current_time}.log'
        """
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        log_filename = os.path.join(Logger.LOG_FOLDER, f"log_info_{current_time}.log")
        print("Logger, log_filename:", log_filename)
        return log_filename

    def _generate_logger_folder_if_not_exists():
        """
        Generates a logger folder if it does not exist
        """
        if not os.path.exists(Logger.LOG_FOLDER):
            os.makedirs(Logger.LOG_FOLDER)