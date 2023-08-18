from pydantic import BaseModel
from typing import Optional, Union, List
from .OptimizationResults import OptimizationResults


class ResultStructure(BaseModel):
    roofTop: Optional[str] = None  # To be decided
    optimization: Optional[List[OptimizationResults]] = None
