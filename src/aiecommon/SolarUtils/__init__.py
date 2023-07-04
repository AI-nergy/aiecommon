from .GetCountryCodeBiddingZone import GetCountryCodeBiddingZone
from ..Models import RequestBody

import json
import logging
import os


class SolarUtils:
    def __init__(self):
        pass
    
    @staticmethod
    def getCountryCode(inputData: RequestBody):
        return GetCountryCodeBiddingZone(inputData).getCountryCodeFromBiddingZone()
