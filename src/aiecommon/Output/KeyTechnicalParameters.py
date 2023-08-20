from pydantic import BaseModel
from typing import Union, Optional


class KeyTechnicalParameters(BaseModel):
    pvCapacity: float
    inverterCapacity: float
    batteryCapacity: float
    yearlySolarPlantProduction: int
    selfSufficiencyYearly: int
    curtailedProductionAbsolute: int
    curtailedProductionPercentage: int
    co2Reduction: int
    estimatedHeatPumpConsumption: Optional[int] = None
    EVplannedConsumption: Optional[int] = None
    EVexistsConsumption: Optional[int] = None
