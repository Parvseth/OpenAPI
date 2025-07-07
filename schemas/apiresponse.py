from pydantic import BaseModel
from typing import Optional, List
from schemas.enums import *






class ApiResponseSchema(BaseModel):

    code: Optional[int]

    type: Optional[str]

    message: Optional[str]


    class Config:
        from_attributes = True