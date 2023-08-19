from pydantic import BaseModel
from typing import Optional, Union, List

class TimeSeries(BaseModel):
    startDateTime: Union[int, str]
    endDateTime: Union[int, str]
    timeResolution: str
    values: List[float]