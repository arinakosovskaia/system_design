from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

    class Config:
        schema_extra = {
            "example": {
                "username": "IvanIvanov2000",
                "password": "qwerty1234",
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "email": "iivanov@gmail.com",
                "phone": "+79999999999"
            }
        }
