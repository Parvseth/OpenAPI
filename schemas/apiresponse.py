from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from schemas.enums import *




class ApiResponseSchema(BaseModel):

    code: Optional[int]

    type: Optional[str]

    message: Optional[str]


    model_config = ConfigDict(from_attributes=True)