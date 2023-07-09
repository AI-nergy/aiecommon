from pydantic import BaseModel
from typing import Optional
from .Technologies import Technologies


class PricesTechnologies(BaseModel):
    fixTerm: Technologies
    variableTerm: Technologies
