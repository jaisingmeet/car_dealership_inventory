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
def test_search_vehicles_by_filters_success():
    token = get_auth_token()
    # Ek Sedan aur ek SUV add karte hain
    client.post("/api/vehicles", json={
        "make": "Honda", "model": "Civic", "year": 2023, "price": 25000.0,
        "status": "available", "category": "Sedan", "quantity": 2
    }, headers={"Authorization": f"Bearer {token}"})
    
    client.post("/api/vehicles", json={
        "make": "Tata", "model": "Harrier", "year": 2024, "price": 35000.0,
        "status": "available", "category": "SUV", "quantity": 1
    }, headers={"Authorization": f"Bearer {token}"})

    # SUV category se filter karke search check karte hain
    response = client.get("/api/vehicles/search?category=SUV", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["model"] == "Harrier"

def test_purchase_vehicle_reduces_quantity():
    token = get_auth_token()
    post_res = client.post("/api/vehicles", json={
        "make": "Hyundai", "model": "Creta", "year": 2024, "price": 20000.0,
        "status": "available", "category": "SUV", "quantity": 3
    }, headers={"Authorization": f"Bearer {token}"})
    v_id = post_res.json()["id"]

    # Purchase endpoint hit karte hain
    response = client.post(f"/api/vehicles/{v_id}/purchase", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["remaining_quantity"] == 2  # 3 mein se 1 kam hona chahiye

def test_restock_vehicle_by_admin_success():
    admin_token = get_auth_token(username="adminmanager", email="adminmgr@example.com", is_admin=True)
    post_res = client.post("/api/vehicles", json={
        "make": "Maruti", "model": "Swift", "year": 2023, "price": 10000.0,
        "status": "available", "category": "Hatchback", "quantity": 1
    }, headers={"Authorization": f"Bearer {admin_token}"})
    v_id = post_res.json()["id"]

    # Admin restock karta hai 4 units
    response = client.post(f"/api/vehicles/{v_id}/restock?amount=4", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["new_quantity"] == 5  # 1 + 4 = 5
    
