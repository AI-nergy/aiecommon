from pydantic import BaseModel
from typing import Optional
from .TimeSeries import TimeSeries

class MeterData(BaseModel):
    pvGeneration: Optional[TimeSeries] = None
    electricityDemand: Optional[TimeSeries] = None