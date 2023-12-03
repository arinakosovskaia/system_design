from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.orm import Session, sessionmaker
from typing import Annotated
from fastapi import Form

from sql_app import models, schemas, crud
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sql_app import models, schemas, crud
from sql_app.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/register")
async def register_user(user: schemas.User, db: Session = Depends(get_db)):
    required_fields = ["email", "password", "first_name", "last_name", "phone", "username"]
    missing_fields = [field for field in required_fields if not getattr(user, field, None)]
    
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")

    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = pwd_context.hash(user.password)
    db_user = crud.create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"status": "ok", "user": db_user}

class BadRequestResponse(BaseModel):
    status: str = "error"
    error: str = "Bad request"

class NotFoundResponse(BaseModel):
    status: str = "error"
    error: str = "User not found"

class UserCreatedResponse(BaseModel):
    status: str = "ok"

@app.post("/order/create", response_model=schemas.Order, responses={
    200: {"description": "Order created"},
    400: {"model": BadRequestResponse, "description": "Bad request"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    created_order = crud.create_order(db=db, order=order, username=user.username)
    if created_order is None:
        raise HTTPException(status_code=400, detail="Incorrect order")
    if user.balance < order.total:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    return created_order.__dict__
    
@app.get("/orders", response_model=List[schemas.Order], responses={
    200: {"description": "List of previous orders"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
async def get_previous_orders(current_user: dict = Depends(get_current_user), skip: int = 0, limit: int = 10, db: Session = Depends(get_db), all: bool = False):
    previous_orders = crud.get_orders(db, current_user.username)
    return previous_orders

@app.post("/billing/deposit", response_model=dict, responses={
    200: {"model": UserCreatedResponse, "description": "Money deposited"},
    400: {"model": BadRequestResponse, "description": "Bad request"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
async def deposit_money(amount: float = Form(...), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user:
        user.balance += amount
        db.commit()
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/billing/balance", response_model=dict, responses={
    200: {"description": "Balance checked"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
async def check_balance(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user:
        return {"status": "ok", "balance": user.balance}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/billing/withdraw", response_model=dict, responses={
    200: {"model": UserCreatedResponse, "description": "Money withdrawn"},
    400: {"model": BadRequestResponse, "description": "Bad request"},
    404: {"model": NotFoundResponse, "description": "User not found"}
})
async def withdraw_money(amount: float = Form(...), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user:
        if user.balance >= amount:
            user.balance -= amount
            db.commit()
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Insufficient funds")
    else:
        raise HTTPException(status_code=404, detail="User not found")
