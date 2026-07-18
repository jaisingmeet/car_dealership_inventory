import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv

from app.database import engine, get_db, Base
from app.models import User, Vehicle
from app.schemas import UserRegister, UserLogin, VehicleCreate, VehicleResponse
from app import crud, auth

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership Inventory API")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-fallback-secret-change-in-prod")
ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except (ExpiredSignatureError, InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# --- AUTH ---

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    crud.create_user(db, user)
    return {"message": "User registered successfully"}

@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, credentials.username)

    if not db_user or not auth.verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {
        "sub": db_user.username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    access_token = encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

# --- VEHICLES ---

@app.post("/api/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def add_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_vehicle = Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@app.get("/api/vehicles", response_model=List[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Vehicle).all()

@app.get("/api/vehicles/search", response_model=List[VehicleResponse])
def search_vehicles(
    make: Optional[str] = None,
    model: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Vehicle)
    if make:
        query = query.filter(Vehicle.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if category:
        query = query.filter(Vehicle.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)
    return query.all()

@app.put("/api/vehicles/{id}", response_model=VehicleResponse)
def update_vehicle(id: int, vehicle_update: VehicleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    for key, value in vehicle_update.model_dump().items():
        setattr(db_vehicle, key, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.delete("/api/vehicles/{id}")
def delete_vehicle(id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}

# --- INVENTORY ---

@app.post("/api/vehicles/{id}/purchase")
def purchase_vehicle(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    if db_vehicle.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle out of stock")

    db_vehicle.quantity -= 1
    if db_vehicle.quantity == 0:
        db_vehicle.status = "out of stock"

    db.commit()
    return {"message": "Purchase successful", "remaining_quantity": db_vehicle.quantity}

@app.post("/api/vehicles/{id}/restock")
def restock_vehicle(id: int, amount: int = 1, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Restock amount must be greater than zero")

    db_vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    db_vehicle.quantity += amount
    if db_vehicle.status == "out of stock":
        db_vehicle.status = "available"

    db.commit()
    return {"message": "Restock successful", "new_quantity": db_vehicle.quantity}