from pydantic import BaseModel
from typing import Optional

class Technologies(BaseModel):
    batteries: float
    pvPanels: float
    inverters: float