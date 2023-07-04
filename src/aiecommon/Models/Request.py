from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .Location import Location


class RequestBody(BaseModel):
    referenceId: int = 324563453232456345323
    location: Location
    yearConsumptionKwh: float = 6500
    ip: str =  '192.169.1.1'
   
    
