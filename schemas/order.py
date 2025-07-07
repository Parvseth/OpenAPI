from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from schemas.enums import *




class OrderSchema(BaseModel):

    id: Optional[int]

    petId: Optional[int]

    quantity: Optional[int]

    shipDate: Optional[str]

    status: Optional[StatusEnum]

    complete: Optional[bool]


    model_config = ConfigDict(from_attributes=True)