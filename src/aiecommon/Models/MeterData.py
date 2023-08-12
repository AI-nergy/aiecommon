from pydantic import BaseModel
from typing import Optional
from .TimeSeries import TimeSeries

class MeterData(BaseModel):
    pvGeneration: TimeSeries
    electricityDemand: TimeSeries