from pydantic import BaseModel, validator
from ..Entities import Rooftop
from aiecommon.Models import Location
from typing import Optional
from aiecommon.Exceptions import AieException

class RequestData(BaseModel):
    referenceId: str
    rooftopSummaryTable: list[Rooftop]
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


    # check that consumption is big enough
    @validator('yearConsumptionKwh', pre=True, allow_reuse=True)
    def check_consumption(cls, v):
        if int(v) < 2500:
            raise AieException(AieException.CONSUMPTION_TOO_LOW)
        return v
