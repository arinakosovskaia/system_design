from sqlalchemy.orm import Session

from . import models, schemas

def create_user(db: Session, user: models.User):
    db_user = models.User(username=user.username, password=user.password, first_name=user.first_name, last_name=user.last_name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

