from .GetCountryCodeBiddingZone import GetCountryCodeBiddingZone
from ..Models import InputData

import json
import logging
import os


class SolarUtils:
    def __init__(self):
        pass
    
    @staticmethod
    def getCountryCode(inputData: InputData):
        return GetCountryCodeBiddingZone(inputData).getCountryCodeFromBiddingZone()
