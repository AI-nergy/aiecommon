from pydantic import BaseModel
from typing import Union, Optional


class KeyTechnicalParameters(BaseModel):
    pvCapacity: float
    inverterCapacity: float
    batteryCapacity: float
    yearlySolarPlantProduction: int
    selfSufficiencyYearly: int
    curtailedProductionAbosulute: int
    curtailedProductionPercentage: int
    co2Reduction: int
    estimatedHeatPumpConsumption: Optional[int]
    EVplannedConsumption: Optional[int]
    EVexistsConsumption: Optional[int]
