from pydantic import BaseModel
from typing import Dict, Optional


class ElectricVehicle(BaseModel):
    batteryCapacity: float
    dischargeEfficiency: float
    chargeEfficiency: float
    maxRelativeDischargeDepth: float
    maxChargingPower: float
    maxDischargingPower: float
