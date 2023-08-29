import logging

class AieException(Exception):

    INVALID_INPUT_DATA = "INVALID_INPUT_DATA"
    INVALID_INPUT_DATA_JSON = "INVALID_INPUT_DATA_JSON"

    GENERIC_PYTHON_ERROR = "GENERIC_PYTHON_ERROR"

    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"

    NO_BUILDING_POLYGON_WIDER_AREA = "NO_BUILDING_POLYGON_WIDER_AREA"
    CONSUMPTION_TOO_LOW = "CONSUMPTION_TOO_LOW"
    NO_BUILDING_POLYGON = "NO_BUILDING_POLYGON"
    ROOFTOP_PLOTTING_ERROR = "ROOFTOP_PLOTTING_ERROR"
    HOUSE_NOT_LOCATED = "HOUSE_NOT_LOCATED"
    HOUSE_TOO_LARGE = "HOUSE_TOO_LARGE"
    ROOFTOP_ALGORITHM_FAILED = "ROOFTOP_ALGORITHM_FAILED"
    BUILDING_NOT_FOUND_ON_OSM = "BUILDING_NOT_FOUND_ON_OSM"
    COUNTRY_NOT_SUPPORTED_FOR_OPTIMIZATION = "COUNTRY_NOT_SUPPORTED_FOR_OPTIMIZATION"
    COUNTRY_NOT_SUPPORTED = "COUNTRY_NOT_SUPPORTED"
    NO_CONSUMPTION_PROVIDED = "NO_CONSUMPTION_PROVIDED"
    MODEL_SOLUTION_NOT_FOUND = "MODEL_SOLUTION_NOT_FOUND"

    log_message: str
    code: str
    data: dict

    def __init__(self, code: str, log_message: str = None, data: dict = None):
        super().__init__(code)

        self.code = code
        self.data = data
        
        if not log_message:
            self.log_message = code
        else:
            self.log_message = log_message

        logging.error(f"AinException notice: self.code={self.code}, self.data={self.data}, self.log_message={self.log_message}")


    def error(self, source):

        return AieException.error(self.code, self.data, source, self.log_message, self)


    @staticmethod
    def error(code, data, source, logMessage = "", exception = None):

        error = AieException(code, logMessage, data)

        logging.info(f"AieException.error: error={error}, logMessage={logMessage}, Exception Name: {type(exception).__name__}, exception={exception}")

        if (exception is not None):
            logging.exception("Caught exception!")

        return error
