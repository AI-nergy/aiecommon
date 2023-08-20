from pydantic import BaseModel, validator
from typing import Optional, Union, List

from ..Exceptions import AieException
from ..Output import ResultStructure, ErrorMessage


class ResponseData(BaseModel):
    success: bool
    result: Optional[ResultStructure] = None
    resultCheckUrl: Optional[str] = None
    errorMessage: Optional[ErrorMessage] = None

    # Validate True success
    @validator('success')
    def validate_success(cls, v, values):
        if v and values['result'] is None:
            raise AieException(AieException.GENERIC_PYTHON_ERROR, "No result provided despite model was successful")

    # Validate False success
    @validator('success')
    def validate_error(cls, v, values):
        if not v and values['errorMessage'] is None:
            raise AieException(AieException.GENERIC_PYTHON_ERROR, "No error message provided despite model failed")
