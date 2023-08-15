import logging

class AieException(Exception):

    INVALID_INPUT_DATA = "INVALID_INPUT_DATA"
    NO_BUILDING_POLYGON_WIDER_AREA = "NO_BUILDING_POLYGON_WIDER_AREA"
    CONSUMPTION_TOO_LOW = "CONSUMPTION_TOO_LOW"
    NO_BUILDING_POLYGON = "NO_BUILDING_POLYGON"
    GENERIC_PYTHON_ERROR = "GENERIC_PYTHON_ERROR"
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

    def __init__(self, error_code: str, log_message: str = None, data: dict = None):
        super().__init__(error_code)

        if not log_message:
            self.log_message = error_code
        else:
            self.log_message = log_message

        logging.info(f"AinException: {self.log_message}")
