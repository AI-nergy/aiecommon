from pydantic import BaseModel
from typing import Optional, Union, List

class ErrorCode(BaseModel):
    rooftopAreaLargerThan: Optional[int]
    radius = Optional[float]
