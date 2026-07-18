# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(title="Car Dealership API")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}