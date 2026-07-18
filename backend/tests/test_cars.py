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
    