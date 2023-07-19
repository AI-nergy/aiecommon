from pydantic import BaseModel
import json 

from ..Models import Photovoltaic, Battery, ElectricVehicle, Inverter
from .RequestData import RequestData
from .data_model_base import DataModelBase

class TechnicalData(DataModelBase):
    Photovoltaic: Photovoltaic
    Battery: Battery
    ElectricVehicle: ElectricVehicle
    Inverter: Inverter

    def from_json_old(path: str, request: RequestData = None):
        return TechnicalData(**json.load(open(path)))