from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register_user():
    response = client.post("/api/auth/register", json={
        "username": "meet", "email": "meet@example.com", "password": "Password123"
    })
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully"}

def test_register_duplicate_email():
    user = {"username": "meet2", "email": "meet@example.com", "password": "Password123"}
    client.post("/api/auth/register", json=user)
    response = client.post("/api/auth/register", json=user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_login_user_success():
    user_data = {
        "username": "login_test_user",
        "email": "login_test@example.com",
        "password": "SecurePassword123",
    }
    client.post("/api/auth/register", json=user_data)

    response = client.post("/api/auth/login", json={
        "username": "login_test_user", "password": "SecurePassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"