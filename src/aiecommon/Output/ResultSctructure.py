from pydantinc import BaseModel
from typing import Optional, Union, List
from .OptimizationResults import OptimizationResults

class ResultStructure(BaseModel):
    roofTop: Optional[str] # To be decided
    optmimization: Optional[List[OptimizationResults]]