from pydantic import BaseModel
from typing import Dict, Optional


class Battery(BaseModel):
    dischargeEffiency: float
    chargeEffiency: float
    maxRelativeDischargeDepth: float
    maxCapacity: float
    minCapacity: float
    chargePowerAsFractionOfBatteryCapacity: float
    dischargePowerAsFractionOfBatteryCapacity: float
    lifetime: int
