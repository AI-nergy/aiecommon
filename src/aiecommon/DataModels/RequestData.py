from pydantic import BaseModel, validator
from ..Models import Rooftop, TechnoEconomicData, MeterData, ElectricVehicle, HeatPump
from aiecommon.Models import Location
from typing import Optional, List
from aiecommon.Exceptions import AieException

class RequestData(BaseModel):
    # Constants
    MINIMUM_YEARLY_CONSUMPTION: Optional[int] = 2500
    # Values
    referenceId: str
    location: Location
    systemType: str
    yearlyConsumption: Optional[float] = None
    meterData: Optional[MeterData] = None
    technoEconomicData: Optional[TechnoEconomicData] = None
    electricVehicle: Optional[ElectricVehicle] = None
    heatPump: Optional[HeatPump] = None
    outputFormat: Optional[str] = None
    rooftopSummaryTable: Optional[List[Rooftop]] = None
    pvOptimizationType: Optional[str] = None


    # check that consumption is big enough
    @validator('yearlyConsumption', pre=True, allow_reuse=True)
    def check_yearly_consumption(cls, v, values):
        if v is None:
            return v
        if int(v) < values["MINIMUM_YEARLY_CONSUMPTION"]:
            raise AieException(AieException.CONSUMPTION_TOO_LOW, data={"minimumConsumption": values["MINIMUM_YEARLY_CONSUMPTION"]})
        return v

    # check that if no meter data is provided, consumption is provided
    @validator('meterData', pre=True, allow_reuse=True)
    def check_meter_data_or_yearly_consumption(cls, v, values):
        if v is None and values['yearlyConsumption'] is None:
            raise AieException(AieException.NO_CONSUMPTION_PROVIDED)
        return v