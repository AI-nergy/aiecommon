
from pydantic import BaseModel

class KeyTechnicalParameters(BaseModel):
    pvCapacity: float
    inverterCapacity: float
    batteryCapacity: float