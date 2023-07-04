from typing import List, Optional, Union

from pydantic import BaseModel


class Location(BaseModel):
    latitude: float = 55.6996798173897
    longitude: float = 12.552480697631838
    zip: Optional[str] = "8930"
    countryCode: Optional[Union[str, None]] = None
    biddingZone: Optional[str]
