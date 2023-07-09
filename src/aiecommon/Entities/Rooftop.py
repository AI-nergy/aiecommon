from pydantic import BaseModel
# from ..Output.Orientation import Orientation

class Rooftop(BaseModel):
    usefulAream2: int
    orientation: str
    orientationDegrees: int
    rooftopSideSlopeDegrees: int