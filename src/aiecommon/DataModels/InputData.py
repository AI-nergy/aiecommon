from pydantic import BaseModel, validator
from typing import Dict, List, Optional, Union

from ..Models import ElectricVehicle, HeatPump, MeterData, Rooftop, TechnoEconomicData, Location
from aiecommon.Exceptions import AieException
from .data_model_base import DataModelBase

class InputData(DataModelBase):
#class InputData(BaseModel):
        # Constants
    MINIMUM_YEARLY_CONSUMPTION: Optional[int] = 2500
    # Values
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
