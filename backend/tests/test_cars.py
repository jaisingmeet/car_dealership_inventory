from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

# Har test run se pehle table clean karne ke liye
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

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
    # Pehle ek car add kar dete hain taaki list mein data ho
    car_data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2023,
        "price": 26000.0,
        "status": "available"
    }
    client.post("/api/cars", json=car_data)
    
    # Ab saari cars fetch karne ke liye GET request bhejte hain
    response = client.get("/api/cars")
    
    # Kyunki GET endpoint abhi bana nahi hai, ye 404 dega aur test FAIL hoga
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["make"] == "Honda"