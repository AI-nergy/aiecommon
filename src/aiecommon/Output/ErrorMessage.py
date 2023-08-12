from pydantic import BaseModel
from typing import Optional, Union, List
from .ErrorCode import ErrorCode

class ErrorMessage(BaseModel):
    code: str
    message: Optional[ErrorCode]