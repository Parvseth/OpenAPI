from pydantic import BaseModel, ConfigDict
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


    model_config = ConfigDict(from_attributes=True)