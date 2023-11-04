from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sql_app import models, schemas, crud

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreatedResponse(schemas.UserResponse):
    status: str = "ok"

class BadRequestResponse(BaseModel):
    status: str = "error"
    error: str = "Bad request"

class NotFoundResponse(BaseModel):
    status: str = "error"
    error: str = "User not found"

@app.get("/health", response_model=str)
def health():
    return "string"

@app.post("/user", response_model=UserCreatedResponse, responses={
    200: {"model": UserCreatedResponse, "description": "User created"},
    400: {"model": BadRequestResponse, "description": "Bad request"}
})
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return {"status": "ok"}

@app.get("/user/{username}", response_model=UserCreatedResponse, responses={
    200: {"description": "User found"},
    400: {"model": BadRequestResponse, "description": "Bad request"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
def get_user(username: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/{username}", response_model=UserCreatedResponse, responses={
    200: {"description": "User found"},
    400: {"model": BadRequestResponse, "description": "Bad request"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
def update_user(username: str, user_data: schemas.User, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username
    user.password = user_data.password
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email
    user.phone = user_data.phone

    db.commit()
    return UserCreatedResponse(**user.dict(), status="ok")

@app.delete("/user/{username}", response_model=UserCreatedResponse, responses={
    200: {"description": "User found"},
    400: {"model": BadRequestResponse, "description": "Bad request"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
def delete_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"status": "ok"}

