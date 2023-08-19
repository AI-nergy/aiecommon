
from pydantic import BaseModel, Field
from typing import List
import pandas as pd

from .HourlyBatteryOperation import HourlyBatteryOperation
from .KeyEconomicIndicators import KeyEconomicIndicators
from .KeyTechnicalParameters import KeyTechnicalParameters
from .Photovoltaic import Photovoltaic
from .Inverter import Inverter
from .InvestmentCostBreakdown import InvestmentCostBreakdown
from .MonthlyBalance import MonthlyBalance
from .HourlyElectricityFlow import HourlyElectricityFlow

class OptimizationResults(BaseModel):
    typeOfResult: str = Field(..., choices=['SYSTEM_OPTIMISATION_TYPE_PV_ONLY', 'SYSTEM_OPTIMISATION_TYPE_BATTERY_ONLY', 'SYSTEM_OPTIMISATION_TYPE_PV_AND_BATTERY'])
    keyEconomicIndicators: KeyEconomicIndicators
    keyTechnicalParameters: KeyTechnicalParameters
    pvPlant: Photovoltaic
    inverter: Inverter
    investmentCostBreakdown: InvestmentCostBreakdown
    monthlyBalanceSummary: List[MonthlyBalance]
    hourlyElectricityFlow: HourlyElectricityFlow
    hourlyBatteryOperation: HourlyBatteryOperation




