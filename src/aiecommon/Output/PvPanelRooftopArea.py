
from pydantic import BaseModel

class PvPanelRooftopArea(BaseModel):
    absolute: int
    percentage: int
    