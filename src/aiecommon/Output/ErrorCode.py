from pydantic import BaseModel
from typing import Optional

class ErrorCode(BaseModel):
    rooftopAreaLargerThan: Optional[int]
    radius = Optional[float]
    class Config:
        arbitrary_types_allowed = True