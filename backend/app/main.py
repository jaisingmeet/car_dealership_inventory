from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from jose import jwt
import bcrypt
from app.database import SessionLocal, engine, Base
from app.models import User, Car
from app.schemas import UserRegister, UserLogin, CarCreate, CarResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership API")

SECRET_KEY = "supersecretkeyforcardealership"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    password_bytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == credentials.username).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    user_password_bytes = credentials.password.encode('utf-8')
    db_password_bytes = db_user.hashed_password.encode('utf-8')
    
    if not bcrypt.checkpw(user_password_bytes, db_password_bytes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token_data = {"sub": db_user.username}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/cars", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def add_car(car: CarCreate, db: Session = Depends(get_db)):
    new_car = Car(
        make=car.make,
        model=car.model,
        year=car.year,
        price=car.price,
        status=car.status
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car