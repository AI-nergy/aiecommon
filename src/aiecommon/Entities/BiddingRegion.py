from pydantic import BaseModel

class BiddingRegion(BaseModel):
    name: str
    regions: list[str] 