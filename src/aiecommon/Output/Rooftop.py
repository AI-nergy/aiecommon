
from pydantic import BaseModel
# from .Orientation import Orientation
from .PvPanelRooftopArea import PvPanelRooftopArea

class Rooftop(BaseModel):
    orientation: str
    numberOfPanelsOnRooftopSide: int
    pvPanelRooftopArea: PvPanelRooftopArea
