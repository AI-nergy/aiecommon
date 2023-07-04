from typing import List, Optional, Union

from pydantic import BaseModel


class Rooftop(BaseModel):
    usefulAream2: int
    orientation: str
    orientationDegrees: int
    rooftopSideSlopeDegrees: int
    colorCode: Optional[str]
