from pydantic import BaseModel
from typing import Dict, Optional

class HeatPump(BaseModel):
    Cop: Optional[float] = 3
    HeatConsumption: Optional[Dict[str, float]]
    areaStructureExisting: Optional[int] = 0
    energyLabelExisting: Optional[str]
    areaStructurePlanned: Optional[int] = 0
    energyLabelPlanned: Optional[str]