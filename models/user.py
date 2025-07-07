from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from db import Base




class User(Base):
    __tablename__ = 'user'


    id = Column(
        Integer, primary_key=True
    )

    username = Column(
        String
    )

    firstName = Column(
        String
    )

    lastName = Column(
        String
    )

    email = Column(
        String
    )

    password = Column(
        String
    )

    phone = Column(
        String
    )

    userStatus = Column(
        Integer
    )
