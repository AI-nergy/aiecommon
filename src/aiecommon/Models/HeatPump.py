from pydantic import BaseModel
from typing import Dict

class HeatPump(BaseModel):
    Cop: float
    HeatConsumption: Dict[str, float]