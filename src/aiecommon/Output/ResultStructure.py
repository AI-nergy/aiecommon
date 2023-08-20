from pydantic import BaseModel
from typing import Optional, Union, List, Dict
from .OptimisationResults import OptimisationResults
from ..DataModels import SystemOptimisationType


class ResultStructure(BaseModel):
    rooftop: Optional[str]  # To be decided
    optimisation: Optional[Dict[SystemOptimisationType, OptimisationResults]] = {}
