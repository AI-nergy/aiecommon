from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    latitude: float
    longitude: float
    countryCode: Optional[str] = None
    biddingZone: Optional[str] = None
    region: Optional[str] = None
