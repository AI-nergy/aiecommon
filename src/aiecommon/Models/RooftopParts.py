from enum import StrEnum
from typing import Dict, Literal

from pydantic import BaseModel

from .Geometry import MultiPolygonModel


class SourceType(StrEnum):
    rooftopDetection = "rooftopDetection"
    editor = "editor"


class OrientationType(StrEnum):
    north = "North"
    north_east = "North-East"
    east = "East"
    south_east = "South-East"
    south = "South"
    south_west = "South-West"
    west = "West"
    north_west = "North-West"
    flat = "Flat"

    @staticmethod
    def from_orientation(angle, slope):
        """Return orientation type corresponding to the given angle and slope"""
        dirs_list = [
            OrientationType.north, 
            OrientationType.north_east,
            OrientationType.east,
            OrientationType.south_east,
            OrientationType.south,
            OrientationType.south_west,
            OrientationType.west,
            OrientationType.north_west,
        ]
        idx = round(angle / (360.0 / len(dirs_list)))
        # select the direction from the list
        dir = dirs_list[idx % len(dirs_list)]
        #
        if slope < 5: # if surface is flat
            dir = OrientationType.flat
        return dir
    

class AreaType(StrEnum):
    rooftopSide = "rooftopSide"
    groundMount = "groundMount"


class PanelInstallationAreaProperties(BaseModel):
    id: int
    featureRole: Literal["panelInstallationArea"] = "panelInstallationArea"
    areaType: AreaType
    
    edgeSpacing: float | None = None
    safetyCorridorSpacing: float | None = None
    panelsRowSpacing: float | None = None
    isSelected: bool
    
    orientation: OrientationType
    usefulAream2: float
    shadedFraction: float | None = None
    orientationDegrees: float
    slopeDegrees: float


class PanelInstallationArea(BaseModel):
    type: Literal["Feature"] = "Feature"
    source: SourceType
    geometry: MultiPolygonModel
    properties: PanelInstallationAreaProperties


class ObstacleProperties(BaseModel):
    id: int
    featureRole: Literal["obstacle"] = "obstacle"

    panelInstallationAreaId: int
    obstacleType: str = "generic"
    width: float | None = None
    height: float | None = None
    spacing: float | None = None


class Obstacle(BaseModel):
    type: Literal["Feature"] = "Feature"
    source: SourceType
    geometry: MultiPolygonModel
    properties: ObstacleProperties