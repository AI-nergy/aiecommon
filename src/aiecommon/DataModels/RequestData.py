from pydantic import BaseModel, validator
from ..Models import Rooftop, TechnoEconomicData, MeterData, ElectricVehicle, HeatPump
from aiecommon.Models import Location
from typing import Optional, List
from aiecommon.Exceptions import AieException

class RequestData(BaseModel):
    referenceId: str
    location: Location
    systemType: str
    yearlyConsumption: Optional[float]
    meterData: Optional[MeterData]
    technoEconomicData: Optional[TechnoEconomicData]
    electricVehicle: Optional[ElectricVehicle]
    heatPump: Optional[HeatPump]
    outputFormat: Optional[str]
    rooftopSummaryTable: Optional[List[Rooftop]]
    pvOptimizationType: Optional[str]

    # check that consumption is big enough
    @validator('yearlyConsumption', pre=True, allow_reuse=True)
    def check_consumption(cls, v):
        if v is None:
            return v
        if int(v) < 2500:
            raise AieException(AieException.CONSUMPTION_TOO_LOW)
        return v

    # check that if no meter data is provided, consumption is provided
    @validator('meterData', pre=True, allow_reuse=True)
    def check_meter_data(cls, v, values):
        if v is None and values['yearlyConsumption'] is None:
            raise AieException(AieException.NO_CONSUMPTION_PROVIDED)
        return v