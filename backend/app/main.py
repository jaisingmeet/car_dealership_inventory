from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt
import bcrypt
from typing import List, Optional
from app.database import SessionLocal, engine, Base
from app.models import User, Vehicle
from app.schemas import UserRegister, UserLogin, VehicleCreate, VehicleResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership Inventory API")

SECRET_KEY = "supersecretkeyforcardelarship"
ALGORITHM = "HS256"

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Token Validation Dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Admin Check Dependency
def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# --- AUTH ENDPOINTS ---

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    password_bytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    # Testing aur ease ke liye: agar username mein 'admin' ho toh automatically admin bana do
    is_admin = True if "admin" in user.username.lower() else False
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == credentials.username).first()
    
    if not db_user or not bcrypt.checkpw(credentials.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token_data = {"sub": db_user.username}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

# --- VEHICLE ENDPOINTS (PROTECTED) ---

@app.post("/api/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def add_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_vehicle = Vehicle(
        make=vehicle.make,
        model=vehicle.model,
        year=vehicle.year,
        price=vehicle.price,
        status=vehicle.status,
        category=vehicle.category,
        quantity=vehicle.quantity
    )
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
    current_user: User = Depends(get_current_user)
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

# --- INVENTORY MANAGEMENT ENDPOINTS ---

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