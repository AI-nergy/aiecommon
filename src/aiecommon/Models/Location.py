from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    latitude: float
    longitude: float


class MainLocation(Location):
    countryCode: Optional[str] = None
    biddingZone: Optional[str] = None
    region: Optional[str] = None
