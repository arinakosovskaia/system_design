from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    balance = Column(Float, default=0.0)

    class Config:
        schema_extra = {
            "example": {
                "username": "IvanIvanov2000",
                "password": "qwerty1234",
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "email": "iivanov@gmail.com",
                "phone": "+79999999999",
                "balance": 0.0
            }
        }


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"))
    items = Column(String)
    total = Column(Float, default=0.0)
    successful = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
