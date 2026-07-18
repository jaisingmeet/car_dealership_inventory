from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)  # Admin authorization ke liye

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default="available")  # available, sold, etc.
    category = Column(String, index=True, nullable=False)  # Sedan, SUV, etc.
    quantity = Column(Integer, default=1)  # Stock management ke liye