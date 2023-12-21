from pydantic import BaseModel
from typing import Optional, Union, List

class TechnoEconomicData(BaseModel):
    pvInvestmentCost: Optional[float] = None # Euro/kWh
    pvWidth: Optional[float] = None #m/panel
    pvLength: Optional[float] = None #m/panel
    pvCapacity: Optional[float] = None # W peak/panel 
    inverterCapacityPrice: Optional[List[List]] = None # EUR/kW
    batteryCapacityPrice: Optional[List[List]] = None # Euro/kWh
    fixedInstallationCost: Optional[float] = None # EUR