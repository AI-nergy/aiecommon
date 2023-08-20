from pydantic import BaseModel
from typing import Optional, Union, List, Dict
from .OptimisationResults import OptimisationResults
from ..DataModels import SystemOptimisationType


class ResultStructure(BaseModel):
    optimisation: Optional[Dict[SystemOptimisationType, OptimisationResults]] = {}
    rooftop: Optional[str] = None  # To be decided