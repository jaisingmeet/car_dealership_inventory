from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from jose import jwt
from app.database import SessionLocal, engine, Base
from app.models import User
from app.schemas import UserRegister, UserLogin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership API")

# JWT configurations
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
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Username se user ko database me search karo
    db_user = db.query(User).filter(User.username == credentials.username).first()
    
    # Check karo user mila ya nahi aur password match hua ya nahi
    if not db_user or db_user.hashed_password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # JWT Access Token banao
    token_data = {"sub": db_user.username}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": access_token, "token_type": "bearer"}