import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

# Helper function jo test ke liye user register karke login token nikal ke dega
def get_auth_token(username="testuser", email="test@example.com", is_admin=False):
    # Registration
    client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": "securepassword123"
    })
    
    # Login to get token
    login_response = client.post("/api/auth/login", json={
        "username": username,
        "password": "securepassword123"
    })
    return login_response.json()["access_token"]

def test_add_vehicle_success():
    token = get_auth_token()
    vehicle_data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2024,
        "price": 32000.0,
        "status": "available",
        "category": "Sedan",
        "quantity": 5
    }
    response = client.post(
        "/api/vehicles", 
        json=vehicle_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["make"] == "Toyota"
    assert response.json()["category"] == "Sedan"
    assert response.json()["quantity"] == 5

def test_get_vehicles_success():
    token = get_auth_token()
    vehicle_data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2023,
        "price": 26000.0,
        "status": "available",
        "category": "Sedan",
        "quantity": 3
    }
    client.post("/api/vehicles", json=vehicle_data, headers={"Authorization": f"Bearer {token}"})
    
    response = client.get("/api/vehicles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["model"] == "Civic"

def test_update_vehicle_success():
    token = get_auth_token()
    initial_vehicle = {
        "make": "Hyundai",
        "model": "i20",
        "year": 2022,
        "price": 12000.0,
        "status": "available",
        "category": "Hatchback",
        "quantity": 2
    }
    post_response = client.post("/api/vehicles", json=initial_vehicle, headers={"Authorization": f"Bearer {token}"})
    vehicle_id = post_response.json()["id"]
    
    updated_data = {
        "make": "Hyundai",
        "model": "i20",
        "year": 2022,
        "price": 11500.0,
        "status": "sold",
        "category": "Hatchback",
        "quantity": 0
    }
    response = client.put(
        f"/api/vehicles/{vehicle_id}", 
        json=updated_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "sold"
    assert response.json()["price"] == 11500.0

def test_delete_vehicle_by_admin_success():
    # Admin token lete hain (Halaanki role logic main.py mein implement hoga)
    token = get_auth_token(username="adminuser", email="admin@example.com", is_admin=True)
    
    vehicle_data = {
        "make": "Ford",
        "model": "Mustang",
        "year": 2023,
        "price": 55000.0,
        "status": "available",
        "category": "Sports",
        "quantity": 1
    }
    post_response = client.post("/api/vehicles", json=vehicle_data, headers={"Authorization": f"Bearer {token}"})
    vehicle_id = post_response.json()["id"]
    
    response = client.delete(f"/api/vehicles/{vehicle_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Vehicle deleted successfully"}
    