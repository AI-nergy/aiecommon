from pydantic import BaseModel
from typing import Dict, Optional


class ElectricVehicle(BaseModel):
    kilometersPerDayExists: float
    kilometersPerDayPlanned: float  
    batteryCapacity: Optional[float]
    dischargeEfficiency: Optional[float]
    chargeEfficiency: Optional[float]
    maxRelativeDischargeDepth: Optional[float]
    maxChargingPower: Optional[float]
    maxDischargingPower: Optional[float]
    

