from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from db import Base



from schemas.enums import StatusEnum


class Pet(Base):
    __tablename__ = 'pet'


    id = Column(
        Integer, primary_key=True
    )

    category = Column(
        Integer
    )

    name = Column(
        String
    )

    photoUrls = Column(
        JSON
    )

    tags = Column(
        JSON
    )

    status = Column(
        Enum(StatusEnum)
    )
