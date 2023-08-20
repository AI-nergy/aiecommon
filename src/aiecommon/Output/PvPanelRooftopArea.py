
from pydantic import BaseModel, validator

class PvPanelRooftopArea(BaseModel):
    absolute: int
    percentage: int

    @validator('absolute', 'percentage', pre=True, always=True)
    def convert_to_int(cls, v):
        return int(v)

