
from pydantic import BaseModel
from typing import List
from .MonthName import MonthName

class MonthlyBalance(BaseModel):
    monthName: str
    selfConsumption: int
    electricitySoldToGrid: int
    electricityBought: int
    pvGeneration: int


