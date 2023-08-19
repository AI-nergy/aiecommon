from pydantic import BaseModel
from typing import Optional, Union, List

class TechnoEconomicData(BaseModel):
    batteryInvestmentCost: Optional[float] = None # Euro/kWh
    pvInvestmentCost: Optional[float] = None # Euro/kWh
    pvArea: Optional[float] = None #m2/panel
    pvCapacity: Optional[float] = None # W peak/panel 
    inverterInvestmentCost: Optional[float] = None # EUR/kW
    fixedInstallationCost: Optional[float] = None # EUR