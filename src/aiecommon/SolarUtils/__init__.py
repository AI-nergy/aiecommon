import json
from fastapi import Request
import traceback

import ..custom_logger
logger = custom_logger.get_logger()
from .Exceptions import AieException

class SolarUtils:

    def __init__(self):
        pass
    
    @staticmethod
    def __pack_error_response(errorMessage, json_dump = False):
        response = {}
        response["success"] = False
        response["errorMessage"] = errorMessage

        return json.dumps(response) if json_dump else response

    @staticmethod
    def __pack_success_response(responseBody, json_dump = False):
        response= {}
        response["success"] = True
        response["result"] = responseBody

        return json.dumps(response) if json_dump else response


    @staticmethod
    def _response(body, status_code):
        from fastapi.responses import JSONResponse
        return JSONResponse(content=body, status_code=status_code)

    @staticmethod
    def error_response(code, data, source, http_error_code, logMessage = "", exception = None):

        errorMessage = {"code": code, "data": data}

        logger.info(f"error_response sent, errorMessage={errorMessage}, http_error_code={http_error_code}")
        logger.error(f"logMessage: {logMessage}")
        custom_logger.dump_debug("ERROR RESPONSE")
        if exception:
            logger.error(f"CAUGHT EXCEPTION: {exception}\nexception.args={exception.args}\nTRACEBACK:\n{traceback.format_exc()}")

        return SolarUtils._response(SolarUtils.__pack_error_response(errorMessage, json_dump=False), http_error_code)

    @staticmethod
    def success_response(result: dict):
        return SolarUtils._response(SolarUtils.__pack_success_response(result, json_dump=False), status_code=200)

    @staticmethod
    def parse_request_body(request: Request) -> dict:
        try:
            request_body_json = request.json()
        except:
            raise AieException(AieException.INVALID_INPUT_DATA, data="Request body is not valid JSON")

        return request_body_json

        # try:
        #     request_body_json = req.get_json()
        # except:
        #     raise AieException(AieException.INVALID_INPUT_DATA, data="Request body is not valid JSON")

        # return request_body_json

    @staticmethod
    def get_timezone_from_country_code(countyCode):
        """
        Load and return the timezone for a given two-letter country code.
        """
        with open('modules/aiesolar/optimizer/data/timeZoneFromCountryCode.json', 'r') as f:
            tzmap = json.load(f)
        return tzmap[countyCode]

    @staticmethod
    def get_tmy_minute_offsets(latitude, longitude, month_year_dict):
        """
        Return a fixed array of minute offsets (8760 entries) for aligning PVGIS TMY timestamps.
        """
        return np.full(8760, 10, dtype=np.float64)