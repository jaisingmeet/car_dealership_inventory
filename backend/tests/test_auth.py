from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_user():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "meet",
            "email": "meet@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 201
    
def test_register_user():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "meet",
            "email": "meet@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "User registered successfully"
    }
