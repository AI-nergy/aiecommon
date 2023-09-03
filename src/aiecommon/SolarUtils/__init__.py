from .GetCountryCodeBiddingZone import GetCountryCodeBiddingZone
from ..Models import InputData

import json
import logging
import os



class SolarUtils:

    def __init__(self, input_data: InputData):
        pass
        self.biddingZone = GetCountryCodeBiddingZone(input_data) 

    def getCountryCode(self):
        return self.biddingZone.getCountryCodeFromBiddingZone()

    def getBiddingZone(self):
        return self.biddingZone._getPolygonBiddingZone()
