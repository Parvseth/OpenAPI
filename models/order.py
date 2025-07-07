from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from db import Base



from schemas.enums import StatusEnum




class Order(Base):
    __tablename__ = 'order'


    id = Column(
        Integer, primary_key=True
    )

    petId = Column(
        Integer
    )

    quantity = Column(
        Integer
    )

    shipDate = Column(
        String
    )

    status = Column(
        Enum(StatusEnum)
    )

    complete = Column(
        Boolean
    )
