from pydantic import BaseModel
from typing import Dict, Optional


class ElectricVehicle(BaseModel):
    kilometersPerDayExists: Optional[float] = None
    kilometersPerDayPlanned: Optional[float] = None
    batteryCapacity: Optional[float] = None
    dischargeEfficiency: Optional[float] = None
    chargeEfficiency: Optional[float] = None
    maxRelativeDischargeDepth: Optional[float] = None
    maxChargingPower: Optional[float] = None
    maxDischargingPower: Optional[float] = None
    

