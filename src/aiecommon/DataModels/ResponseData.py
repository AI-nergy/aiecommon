from pydantic import BaseModel
from typing import Optional, Union, List
from ..Output import ResultStructure, ErrorMessage

class ResponseData(BaseModel):
    success: Optional[bool]
    result: Optional[ResultStructure]
    errorMessage: Optional[ErrorMessage]