from fastapi import FastAPI, status
from app.schemas import UserRegister

app = FastAPI(title="Car Dealership API")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    return {
        "message": "User registered successfully"
    }