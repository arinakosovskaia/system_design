from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import datetime

class User(BaseModel):
    username: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    phone: str = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "IvanIvanov2000",
                "password": "qwerty1234",
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "email": "iivanov@gmail.com",
                "phone": "+79999999999"
            }
        }

class OrderBase(BaseModel):
    items: Optional[str]
    total: float = None

class OrderCreate(OrderBase):
    class Config:
            schema_extra = {
                "example": {
                    "items": "item1",
                    "total": 100.0
                }
            }
        
class Order(OrderBase):
    id: int
    username: str
    items: Optional[str]
    total: float
    successful: bool
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    username: str = None
    password: str = None
