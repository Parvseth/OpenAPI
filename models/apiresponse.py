from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from db import Base




class ApiResponse(Base):
    __tablename__ = 'apiresponse'


    code = Column(
        Integer, primary_key=True
    )

    type = Column(
        String
    )

    message = Column(
        String
    )
