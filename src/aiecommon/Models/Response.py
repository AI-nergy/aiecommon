from typing import List, Optional, Union

from pydantic import BaseModel

from .Request import RequestBody
from .Rooftop import Rooftop


class ResponseBody(BaseModel):
    referenceId: str
    typeOfResult: str
    countryCode: str
    biddingZone: str
    rooftopSummaryTable: List[Rooftop]
    rooftopModelFigure: str
    housePolygon: List[List[float]]
