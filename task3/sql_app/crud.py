from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas

def create_user(db: Session, user: schemas.User):
    try:
        db_user = models.User(username=user.username, password=user.password, first_name=user.first_name, last_name=user.last_name, email=user.email, phone=user.phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        return None

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_orders(db: Session, username: str, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.username == username).offset(skip).limit(limit).all()

def deposit_money(db: Session, username: str, amount: float):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.balance += amount
        db.commit()
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "User not found"}

def check_balance(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return {"status": "ok", "balance": user.balance}
    else:
        return {"status": "error", "message": "User not found"}

def withdraw_money(db: Session, username: str, amount: float):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        if user.balance >= amount:
            user.balance -= amount
            db.commit()
            return {"status": "ok"}
        else:
            return {"status": "error", "message": "Insufficient funds"}
    else:
        return {"status": "error", "message": "User not found"}

def create_order(db: Session, order: schemas.OrderCreate, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return {"status": "error", "message": "User not found"}
    if user.balance >= order.total:
        user.balance -= order.total
        try:
            db_order = models.Order(**order.dict(), username=username, successful=True)
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            return db_order
        except IntegrityError as e:
            db.rollback()
            return None
    else:
        try:
            db_order = models.Order(**order.dict(), username=username, successful=False)
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            return {"status": "error", "message": "Insufficient funds"}
        except IntegrityError as e:
            db.rollback()
            return None

def get_orders_by_username(db: Session, username: str, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.username == username).offset(skip).limit(limit).all()

def get_previous_orders(db: Session, username: str, skip: int = 0, limit: int = 10, all: bool = False):
    if all:
        return db.query(models.Order).filter(
            models.Order.username == username
        ).offset(skip).limit(limit).all()
    else:
        return db.query(models.Order).filter(
            models.Order.username == username,
            models.Order.successful == True
        ).offset(skip).limit(limit).all()

