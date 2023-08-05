
from pydantic import BaseModel

class KeyTechnicalParameters(BaseModel):
    pvCapacity: float
    inverterCapacity: float
    batteryCapacity: float
    yearlySolarPlantProduction: int
    selfSufficiencyYearly: float
    curtailedProduction: Union[int, float]
    co2Reduction: float

