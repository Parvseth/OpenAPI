from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from schemas.enums import *



from schemas.category import CategorySchema


class PetSchema(BaseModel):

    id: Optional[int]

    category: Optional[CategorySchema]

    name: str

    photoUrls: str

    tags: Optional[str]

    status: Optional[StatusEnum]


    model_config = ConfigDict(from_attributes=True)