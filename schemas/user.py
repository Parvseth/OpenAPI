from pydantic import BaseModel
from typing import Optional, List
from schemas.enums import *






class UserSchema(BaseModel):

    id: Optional[int]

    username: Optional[str]

    firstName: Optional[str]

    lastName: Optional[str]

    email: Optional[str]

    password: Optional[str]

    phone: Optional[str]

    userStatus: Optional[int]


    class Config:
        from_attributes = True