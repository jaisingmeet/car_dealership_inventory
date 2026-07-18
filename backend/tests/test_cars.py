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
    
    # Kyunki endpoint abhi bana nahi hai, ye fail hoga (404 Not Found)
    assert response.status_code == 201
    assert response.json()["make"] == "Toyota"
    assert "id" in response.json()