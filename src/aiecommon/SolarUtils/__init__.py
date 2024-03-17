import json
import azure.functions as func
import traceback
from ..Logger import Logger

from aiecommon.Exceptions import AieException

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
        return func.HttpResponse(body=body, status_code=status_code, headers={"Content-Type": "application/json"})


    @staticmethod
    def error_response(code, data, source, http_error_code, logMessage = "", exception = None):

        errorMessage = {"code": code, "data": data}

        Logger.info(f"error_response sent, errorMessage={errorMessage}, http_error_code={http_error_code}")
        Logger.error(f"logMessage: {logMessage}")
        Logger.dump_debug("ERROR RESPONSE")
        if exception:
            Logger.error(f"CAUGHT EXCEPTION: {exception}\nexception.args={exception.args}\nTRACEBACK:\n{traceback.format_exc()}")

        return SolarUtils._response(SolarUtils.__pack_error_response(errorMessage, True), http_error_code)

    @staticmethod
    def success_response(result: dict):
        return SolarUtils._response(SolarUtils.__pack_success_response(result, json_dump=True), status_code=200)


    @staticmethod
    def call_endpoint(endpoint:str, params:dict=None, method="GET", request_body=None, safe_result=True, file_sufix = None):
        import azure.functions as func
        import function_app as app

        endpoint = endpoint.replace("/", "_")
        request_body = json.dumps(request_body).encode('utf-8')
 
        req = func.HttpRequest(method=method, url="", params=params, body=request_body)
        response = getattr(app, endpoint)._function._func(req)
        response_body = json.loads(response.get_body())
 
        Logger.info("response_body:")
        Logger.info(response_body)
    
        if safe_result:
            file_name = f"runtimedata/output_{file_sufix + '_' if file_sufix else ''}{endpoint}.json"
            json.dump(response_body, open(file_name, "w"))
    
        return response_body

    @staticmethod
    def parse_request_body(req: func.HttpRequest) -> dict:

        try:
            request_body_json = req.get_json()
        except:
            raise AieException(AieException.INVALID_INPUT_DATA, data="Request body is not valid JSON")

        return request_body_json
