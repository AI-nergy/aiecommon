from pydantic import BaseModel, validator
from typing import Dict, List, Optional, Union
import numpy as np

from ..Models import ElectricVehicle, HeatPump, MeterData, Rooftop, TechnoEconomicData, Location, ResponseBody
from aiecommon.Exceptions import AieException
from ..DataModels import SystemOptimisationType
from ..DataModels.data_model_base import DataModelBase

MINIMUM_YEARLY_CONSUMPTION = 2500

class InputData(DataModelBase):
#class InputData(BaseModel):
        # Constants
    # Values

    # siteIdentifier is temporary until we eliminate POST and change SolarPlanner website to use poling
    siteIdentifier: Optional[str]

    referenceId: str
    location: Location
    systemType: Optional[str]
    requestedOptimisationTypes: Optional[List[SystemOptimisationType]]
    yearlyConsumption: Optional[float]
    meterData: Optional[MeterData]
    technoEconomicData: Optional[TechnoEconomicData]
    electricVehicle: Optional[ElectricVehicle]
    heatPump: Optional[HeatPump]
    outputFormat: Optional[str]
    rooftopResult: Optional[ResponseBody] 
    
    # Private Values (not published in the API)
    resultOptimizationType: Optional[SystemOptimisationType]

    # Needed only for SolarPLanner, until we upgrade it to polling instead of POST
    # We don't publish this field in the API documentation
    callbackUrl: Optional[str]

    # TODONACHO: CONSUMPTION_TOO_LOW shouldn't be an error
    # Actually, implement better error handling in the API response, separate errors for rooftop and optimiser
    # check that consumption is big enough
    @validator('yearlyConsumption', pre=True, allow_reuse=True)
    def check_yearly_consumption(cls, v, values):
        if v is None:
            return v
        if int(v) < MINIMUM_YEARLY_CONSUMPTION:
            raise AieException(AieException.CONSUMPTION_TOO_LOW, data={"minimumConsumption": MINIMUM_YEARLY_CONSUMPTION})
        return v

    # check that if no meter data is provided, consumption is provided
    @validator('meterData', pre=True, allow_reuse=True)
    def check_meter_data_or_yearly_consumption(cls, v, values):
        if v is None and values['yearlyConsumption'] is None:
            raise AieException(AieException.NO_CONSUMPTION_PROVIDED)
        return v   

    # check that resultOptimizationType is among the optimization types which don't need rooftop data, or rooftop data is provided
    @validator('resultOptimizationType', pre=True, allow_reuse=True)
    def check_result_optimisation_type_and_rooftop_result(cls, v, values):
        if v is not None and v not in SystemOptimisationType.optimizationOnlyAllowedTypes() and ('rooftopResult' not in values or not values['rooftopResult']):
            raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "requestedOptimisationTypes", "message": f"For system optimization {v} we need to run rooftop first. Please use only {SystemOptimisationType.optimizationOnlyAllowedTypes()} with /solar/optmizer, or use '/solar' API endpoint for other optimization types."})
        return v   

    # check that non-negativity of technoEconomicData
    @validator('technoEconomicData', pre=True, allow_reuse=True)
    def check_techno_economic_data(cls, v, values):
        if v is not None:
            if v['pvInvestmentCost'] <= 0.0: 
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "pvInvestmentCost", "message": f"pvInvestmentCost must be greater than 0.0"})
            if v['pvWidth'] <= 0.0: 
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "pvWidth", "message": f"pvWidth must be greater than 0.0"})
            if v['pvLength'] <= 0.0: 
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "pvLength", "message": f"pvLength must be greater than 0.0"})
            if v['pvCapacity'] <= 0.0: 
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "pvCapacity", "message": f"pvCapacity must be greater than 0.0"})
            if (np.array(v['inverterCapacityPrice']) < 0.0).any():
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "inverterCapacityPrice", "message": f"all entries of inverterCapacityPrice must be greater than 0.0"})
            if (np.array(v['batteryCapacityPrice']) < 0.0).any():
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "batteryCapacityPrice", "message": f"all entries of batteryCapacityPrice must be greater than 0.0"})
            if v['fixedInstallationCost'] < 0.0: 
                raise AieException(AieException.INVALID_INPUT_DATA, "", {"field": "fixedInstallationCost", "message": f"fixedInstallationCost must be equal or greater than 0.0"})

    class Config:
#        validate_assignment = True
        pass