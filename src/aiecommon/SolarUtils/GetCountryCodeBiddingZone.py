# source of geojson files
# https://github.com/EnergieID/entsoe-py/tree/master/entsoe/geo/geojson
import json
import numpy as np
import matplotlib.path as mpltPath
import logging


from aiecommon.Models import InputData
from aiecommon.FileSystem import LocalDataFiles

#         return GetCountryCodeBiddingZone(inputData).getCountryCodeFromBiddingZone()

# TODO: what to do with this:
#
# check that the country is supported
# with open("modules/aiesolar/rooftop/data/supportedCountries.json") as data:
#     supportedCountries = json.load(data)
#     if SolarUtils.getCountryCode(InputData(**orchestratorInput["inputData"])) not in supportedCountries["supportedCountries"]:
#         return Utils.ErrorResponse("Country not supported", Utils.ERROR_RESPONSE_INPUT_VALIDATION, 400)
#
#

class GetCountryCodeBiddingZone:
    def __init__(self, request: InputData) -> None:

        self.request = request

        #self.polygons = json.load(open("modules/aiesolar/rooftop/data/biddingZonesPolygonsFiltered.json"))
        #self.polygons = json.load(importlib.resources.files("aiecommon").joinpath("data/biddingZonesPolygonsFiltered.json").open())
        self.polygons = LocalDataFiles.load_json("data/biddingZonesPolygonsFiltered.json", "aiecommon")

        # crs is only metadata and not a polygon, so we need to delete it for calculations
        del self.polygons["crs"]
        #self.countryCodeBiddingZone = json.load(open("modules/aiesolar/rooftop/data/countryCodeBiddingZone.json"))
        #self.countryCodeBiddingZone = json.load(importlib.resources.files("aiecommon").joinpath("data/countryCodeBiddingZone.json").open())
        self.countryCodeBiddingZone = LocalDataFiles.load_json("data/countryCodeBiddingZone.json", "aiecommon")

    # this function returns bidding zone based on coordinates, and 501 error if the requested location is not implemented yet
    def _getPolygonBiddingZone(self):  # sourcery skip: raise-specific-error        
        logging.info(f"self.request: {self.request}")
        point = [
            (self.request.location.longitude, self.request.location.latitude)
        ]  # because crs84 is in lon, lat, otherwise it is the same as epsg4326
        filteredGeoJSON = self.polygons
        biddingZone = None
        # looping biding zone by bidding zone
        for key, value in filteredGeoJSON.items():
            # each bidding zone can be multipolygon or a single polygon, so we need to loop through all of them, but it can also be a single polygon
            if len(filteredGeoJSON[key]) == 1:
                poly = np.array(filteredGeoJSON[key][0])
                if mpltPath.Path(poly).contains_points(point)[0] == True:
                    biddingZone = key
            else:
                for i in range(len(filteredGeoJSON[key])):
                    poly = np.array(filteredGeoJSON[key][i][0])
                    if mpltPath.Path(poly).contains_points(point)[0] == True:
                        biddingZone = key
                    # we also break the loop as we found our bidding zone
        return biddingZone.upper() if biddingZone else None

    # this function maps bidding zone to the country from predefined json file
    def getCountryCodeFromBiddingZone(self):
        # call bidding zone function
        self.request.location.biddingZone = self._getPolygonBiddingZone()
        if not self.request.location.biddingZone:
            return None
        for key, values in self.countryCodeBiddingZone.items():
            if self.request.location.biddingZone in values:
                self.request.location.countryCode = key
                return key
