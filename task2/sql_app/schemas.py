from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: Optional[str]
    first_name: str
    last_name: str
    email: str
    phone: str
    
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

class UserResponse(BaseModel):
    username: str
    password: Optional[str]
    first_name: str
    last_name: str
    email: str
    phone: str

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
