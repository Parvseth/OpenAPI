from pydantic import BaseModel
from typing import Optional, List
from schemas.enums import *




from schemas.category import CategorySchema



class PetSchema(BaseModel):

    id: Optional[int]

    category: Optional[CategorySchema]

    name: str

    photoUrls: List[str]

    tags: Optional[List[str]]

    status: Optional[StatusEnum]


    class Config:
        from_attributes = True