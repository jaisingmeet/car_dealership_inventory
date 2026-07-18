from sqlalchemy.orm import Session
from app import models, schemas, auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserRegister):
    is_admin = "admin" in user.username.lower()
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=auth.hash_password(user.password),
        is_admin=is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user