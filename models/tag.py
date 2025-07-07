from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from db import Base




class Tag(Base):
    __tablename__ = 'tag'


    id = Column(
        Integer, primary_key=True
    )

    name = Column(
        String
    )
