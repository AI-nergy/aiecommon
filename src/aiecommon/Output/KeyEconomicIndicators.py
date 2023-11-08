
from pydantic import BaseModel
from typing import Optional

class KeyEconomicIndicators(BaseModel):
    payBackPeriod: Optional[float] = None
    totalInvestmentAfterSubsidy: int
    monthlySavingsAfterLoanPayment: int
    constantCosts: int