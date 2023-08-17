from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .Location import Location

class InputDataOLD(BaseModel):
    referenceId: str
    location: Location
    yearConsumptionKwh: float
    pvOptimizationType: Optional[str] = None
    electricVehiclePlanned: bool
    kilometersPerDayPlanned: Optional[float] = 35  
    electricVehicleExists: bool
    kilometersPerDayExists: Optional[float] = 35 # TODO: Ask Dominik why why need this data, if we already know the consumption from the smart meter profile? maybe to stimate?
    heatPumpExists: bool
    heatPumpPlanned: bool
    ipAddress: Optional[str]
    areaStructureHPExists: Optional[int]
    energyLabelHPExists: Optional[str]
    areaStructureHPPlanned: Optional[int]
    energyLabelHPPlanned: Optional[str]

    
