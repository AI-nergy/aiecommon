from pydantic import BaseModel, Field
from typing import Optional, List, ClassVar

class RooftopSide(BaseModel):

    id: Optional[int] = None
    usefulAream2: int
    orientation: str
    orientationDegrees: int
    rooftopSideSlopeDegrees: int
    colorCode: Optional[str] = None
    geometry: Optional[dict] = None
    rooftopShadingHourly: Optional[List[int]] = None
    shadedFraction: Optional[float] = None

