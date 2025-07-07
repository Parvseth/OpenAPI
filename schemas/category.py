from pydantic import BaseModel
from typing import Optional, List
from schemas.enums import *






class CategorySchema(BaseModel):

    id: Optional[int]

    name: Optional[str]


    class Config:
        from_attributes = True