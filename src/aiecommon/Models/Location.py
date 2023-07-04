from pydantic import BaseModel
from typing import Optional


class Location(BaseModel):
    latitude: float
    longitude: float
    countryCode: Optional[str]
    biddingZone: Optional[str]
