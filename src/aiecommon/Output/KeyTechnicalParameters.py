from pydantic import BaseModel
from typing import Union, Optional


class KeyTechnicalParameters(BaseModel):
    pvCapacity: float
    inverterCapacity: float
    batteryCapacity: float
    yearlySolarPlantProduction: int
    selfSufficiencyYearly: float
    curtailedProduction: Union[int, float]
    co2Reduction: float
    estimatedHeatPumpConsumption: Optional[int]
    EVplannedConsumption: Optional[int]
    EVexistsConsumption: Optional[int]
