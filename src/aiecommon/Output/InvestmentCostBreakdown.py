
from pydantic import BaseModel
from .CostBreakdown import CostBreakdown

class InvestmentCostBreakdown(BaseModel):
    pvInvestment: CostBreakdown
    inverterInvestment: CostBreakdown
    batteryInvestment: CostBreakdown
    otherCosts: CostBreakdown