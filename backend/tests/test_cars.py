import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Yeh fixture har ek test function se pehle database ko automatic saaf karega
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_add_car_success():
    car_data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2024,
        "price": 32000.0,
        "status": "available"
    }
    response = client.post("/api/cars", json=car_data)
    assert response.status_code == 201
    assert response.json()["make"] == "Toyota"
    assert "id" in response.json()

def test_get_cars_success():
    # Ab har test ka apna fresh DB hoga, toh ye pehli hi car hogi
    car_data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2023,
        "price": 26000.0,
        "status": "available"
    }
    client.post("/api/cars", json=car_data)
    
    response = client.get("/api/cars")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["make"] == "Honda"

def test_filter_cars_by_make_success():
    # 1. Pehle do alag-alag companies ki cars add karte hain
    client.post("/api/cars", json={
        "make": "Toyota",
        "model": "Camry",
        "year": 2024,
        "price": 32000.0,
        "status": "available"
    })
    client.post("/api/cars", json={
        "make": "Honda",
        "model": "Civic",
        "year": 2023,
        "price": 26000.0,
        "status": "available"
    })
    
    # 2. Ab sirf Toyota filter karne ke liye query parameter ke sath GET request bhejte hain
    response = client.get("/api/cars?make=Toyota")
    
    # 3. Assertions (Kyunki filtering abhi implement nahi hui hai, ye test FAIL hoga)
    assert response.status_code == 200
    cars = response.json()
    assert len(cars) == 1  # Sirf 1 car aani chahiye (Toyota)
    assert cars[0]["make"] == "Toyota"
def test_update_car_success():
    # 1. Pehle ek car add karte hain jise baad mein update karenge
    initial_car = {
        "make": "Hyundai",
        "model": "i20",
        "year": 2022,
        "price": 12000.0,
        "status": "available"
    }
    post_response = client.post("/api/cars", json=initial_car)
    car_id = post_response.json()["id"]
    
    # 2. Updated data taiyar karte hain (status "sold" aur price badal di)
    updated_data = {
        "make": "Hyundai",
        "model": "i20",
        "year": 2022,
        "price": 11500.0,
        "status": "sold"
    }
    
    # 3. PUT request bhejte hain specific car_id par
    response = client.put(f"/api/cars/{car_id}", json=updated_data)
    
    # 4. Assertions (Kyunki endpoint abhi bana nahi hai, ye test 404/405 dekar FAIL hoga)
    assert response.status_code == 200
    assert response.json()["status"] == "sold"
    assert response.json()["price"] == 11500.0
def test_delete_car_success():
    # 1. Pehle ek car add karte hain jise delete karna hai
    car_data = {
        "make": "Ford",
        "model": "Mustang",
        "year": 2023,
        "price": 55000.0,
        "status": "available"
    }
    post_response = client.post("/api/cars", json=car_data)
    car_id = post_response.json()["id"]
    
    # 2. DELETE request bhejte hain us specific car_id par
    response = client.delete(f"/api/cars/{car_id}")
    
    # 3. Assertions (Kyunki endpoint abhi bana nahi hai, ye test FAIL hoga)
    assert response.status_code == 200
    assert response.json() == {"message": "Car deleted successfully"}
    
    # 4. Verify karne ke liye saari cars fetch karte hain, list khali honi chahiye
    get_response = client.get("/api/cars")
    assert len(get_response.json()) == 0
