from pydantic import BaseModel
import pandas as pd
from typing import List, Optional

class HourlyBatteryOperation(BaseModel):
    columns: Optional[List[str]] = ["batteryInflow", "batteryOutflow", "batteryLevel"]
    data: List[List[float]]