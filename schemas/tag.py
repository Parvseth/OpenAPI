from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from schemas.enums import *




class TagSchema(BaseModel):

    id: Optional[int]

    name: Optional[str]


    model_config = ConfigDict(from_attributes=True)