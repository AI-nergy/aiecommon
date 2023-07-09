
from pydantic import BaseModel
from typing import List
from .Rooftop import Rooftop

class Photovoltaic(BaseModel):
    totalNumberOfPanels: int
    rooftopSides: List[Rooftop]
