from pydantic import BaseModel
from typing import Dict, Optional
from ..Entities import Photovoltaic, Battery, ElectricVehicle, Inverter
from .RequestData import RequestData
import json 

class TechnicalData(BaseModel):
    Photovoltaic: Photovoltaic
    Battery: Battery
    ElectricVehicle: ElectricVehicle
    Inverter: Inverter

    def from_json(path: str, request: RequestData = None):
        return TechnicalData(**json.load(open(path)))