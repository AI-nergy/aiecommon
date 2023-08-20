from typing import List, Optional

from pydantic import BaseModel


class Country(BaseModel):
    countryCode: str
    EPSG: int
    UTM: Optional[int] = None
    resolution: Optional[float] = 0.4
    mapName: Optional[str] = "{}.{}.tif"
    mapCoordResolution: Optional[int] = 3
    tileResolutionX: int
    tileResolutionY: int
    mapNameYX: Optional[bool] = False
    boundingPolyXY: bool
    folderId: str
    fileMapName: str
    buildingPolygonsNameFile: Optional[str] = None
    PolyNameYX:  Optional[bool] = False
    buildingPolygonsEPSG: Optional[int] = None
    buildingPolygonsResolution: Optional[int] = None
