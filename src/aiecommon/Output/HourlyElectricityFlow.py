
from pydantic import BaseModel
import pandas as pd
from typing import List

class HourlyElectricityFlow(BaseModel):
    columns: List[str] = ["electricityFromGrid", "electricityToGrid", "pvGeneration", "electricityDemand"]
    data: List[List[float]]