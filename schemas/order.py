from pydantic import BaseModel
from typing import Optional, List
from schemas.enums import *






class OrderSchema(BaseModel):

    id: Optional[int]

    petId: Optional[int]

    quantity: Optional[int]

    shipDate: Optional[str]

    status: Optional[StatusEnum]

    complete: Optional[bool]


    class Config:
        from_attributes = True