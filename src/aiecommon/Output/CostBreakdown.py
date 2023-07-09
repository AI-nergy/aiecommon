
from pydantic import BaseModel

class CostBreakdown(BaseModel):
    absolute: int
    percentage: int