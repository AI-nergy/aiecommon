from pydantic import BaseModel
import json 
from typing import Optional
from ..Models import Photovoltaic, Battery, ElectricVehicle, Inverter, HeatPump
from .data_model_base import DataModelBase

class TechnicalData(DataModelBase):
    Photovoltaic: Optional[Photovoltaic]
    Battery: Optional[Battery]
    ElectricVehicle: Optional[ElectricVehicle]
    Inverter: Optional[Inverter]
    HeatPump: Optional[HeatPump]
