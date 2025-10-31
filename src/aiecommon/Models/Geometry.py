from typing import Any, List, Literal

from pydantic import BaseModel
from shapely import Polygon, MultiPolygon


def _coordlist_from_polygon(poly):
    assert isinstance(poly, Polygon), "poly must be shapely.Polygon"
    coords = [[list(c) for c in poly.exterior.coords]]
    for ring in poly.interiors:
        coords.append(
            [list(c) for c in ring.coords]
        )
    return coords


class GeometryModel(BaseModel):
    type: str  # e.g., "Polygon", "MultiPolygon"
    coordinates: Any


class PolygonModel(GeometryModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]]

    
    @staticmethod
    def from_shapely(poly):
        assert isinstance(poly, Polygon), "input must be shapely.Polygon"
        return PolygonModel(coordinates=_coordlist_from_polygon(poly))


class MultiPolygonModel(GeometryModel):
    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: List[List[List[List[float]]]]

    
    @staticmethod
    def from_shapely(multipoly):
        assert isinstance(multipoly, MultiPolygon), \
            "input must be shapely.MultiPolyhon"
        return MultiPolygonModel(
            coordinates=[_coordlist_from_polygon(p) for p in multipoly.geoms]
        )
    