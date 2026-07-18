# backend/app/main.py
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User
from app.schemas import UserRegister

# Real database tables create karne ke liye (agar exist nahi karti toh)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership API")

# Database dependency (har request ke liye session open aur close karne ke liye)
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
    # 1. Check karo ki email database mein already hai ya nahi
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Naya user object banao (Abhi bina password hash ke, just functionality test karne ke liye)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # Abhi direct save kar rahe hain next step me hash karenge
    )
    
    # 3. Database me save karo
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}
