import logging
import json
import importlib.resources
from .FileSystem  import LocalDataFiles
import aiecommon

class AieError():
    
    ERROR_EXCEPTION_AINERGY: str = "errorAinergy"
    ERROR_EXCEPTION_PYTHON: str = "errorPython"
    ERROR_INPUT_VALIDATION: str = "inputValidation"

#    translations = json.load(importlib.resources.files("aiecommon").joinpath("data/translations.json").open())
#    translations = json.load(FileSystem.open_file("translations.json", FileSystem.LocalDataFiles))
#    translations = json.load(FileSystem.LocalDataFiles.open_file("data/translations.json", "aiecommon"))
    translations = LocalDataFiles.load_json("data/translations.json", aiecommon)

    def __init__(self, error, code, message, source = "NO SET"):

        self.error  = error
        self.message = message
        self.source = source
        self.code = code

    @staticmethod
    def translateErrorMessage(message):
        if message in AieError.translations:
            return AieError.translations[message]
        else:
            return message

    @staticmethod
    def error(error, code, source, exception = None):
        errorDict = AieError(error, code, AieError.translateErrorMessage(code), source).__dict__

        logging.info(f"AieError occured: {errorDict}, Exception Name: {type(exception).__name__}, exception={exception}")

        if (exception is not None):
            logging.exception("Caught exception:")

        return errorDict
