from pydantic import BaseModel
from typing import Optional

class SurfaceCapacityRatio(BaseModel):
    intercept: float
    slope: float