# source of geojson files
# https://github.com/EnergieID/entsoe-py/tree/master/entsoe/geo/geojson
import json
import numpy as np
import matplotlib.path as mpltPath
import logging


from aiecommon.Models import InputData
from aiecommon.FileSystem import LocalDataFiles

#         return GetCountryCodeBiddingZone(inputData).getCountryCodeFromBiddingZone()


class GetCountryCodeBiddingZone:
    def __init__(self, input_data: InputData) -> None:

        self.input_data = input_data

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
        # logging.info(f"self.input_data: {self.input_data}")
        point = [
            (self.input_data.location.longitude, self.input_data.location.latitude)
        ]  # because crs84 is in lon, lat, otherwise it is the same as epsg4326
        filteredGeoJSON = self.polygons
        biddingZone = None

        # 1. Check simple polygons
        for key, value in filteredGeoJSON.items():
            if len(value) == 1 and not isinstance(value[0][0][0], list):  # Simple Polygon
                poly = np.array(value[0])
                if mpltPath.Path(poly).contains_points(point)[0]:
                    biddingZone = key.upper()
                    break

        # 2. If biddingZone not found in simple polygons, check multipolygons
        if not biddingZone:
            for key, value in filteredGeoJSON.items():
                # Skip simple polygons
                if len(value) == 1 and not isinstance(value[0][0][0], list):
                    continue

                # Check for Multipolygon (nested lists)
                for poly_data in value:
                    if isinstance(poly_data[0][0], list) and isinstance(poly_data[0][0][0], list):
                        for sub_poly in poly_data:
                            while isinstance(sub_poly[0][0], list):
                                sub_poly = sub_poly[0]
                            poly = np.array(sub_poly)
                            if mpltPath.Path(poly).contains_points(point)[0]:
                                biddingZone = key.upper()
                                break
                    else:  # Simple polygon structure within multipolygon (outer boundary)
                        current_level = poly_data
                        while isinstance(current_level, list):
                            current_level = current_level[0]
                        while isinstance(poly_data[0][0], list):
                            poly_data = poly_data[0]
                        poly = np.array(poly_data)
                        if mpltPath.Path(poly).contains_points(point)[0]:
                            biddingZone = key.upper()
                            break

                if biddingZone:  # check if biddingZone was set in inner loop
                    break  # break outer loop

        logging.info(f"biddingZone={biddingZone}")
        return biddingZone.upper() if biddingZone else None

    # this function maps bidding zone to the country from predefined json file
    def getCountryCodeFromBiddingZone(self):
        # call bidding zone function
        self.input_data.location.biddingZone = self._getPolygonBiddingZone()
        if not self.input_data.location.biddingZone:
            return None
        for key, values in self.countryCodeBiddingZone.items():
            if self.input_data.location.biddingZone in values:
                self.input_data.location.countryCode = key
                logging.info(f"countryCode={key}")
                return key