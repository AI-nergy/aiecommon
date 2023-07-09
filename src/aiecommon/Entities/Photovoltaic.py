from pydantic import BaseModel
from typing import Dict, Optional
from .SurfaceCapacityRatio import SurfaceCapacityRatio

class Photovoltaic(BaseModel):

    # TODO: this should be result of user input - how?
    minSizeOnRoofSide: float
    surfaceCapacityRatio: SurfaceCapacityRatio
    labourHours: int
    lifetime: int
    kwPerPanel: float
    sqmPerPanel: float
