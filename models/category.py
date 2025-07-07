from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from db import Base






class Category(Base):
    __tablename__ = 'category'


    id = Column(
        Integer, primary_key=True
    )

    name = Column(
        String
    )
