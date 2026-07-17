# backend/tests/test_auth.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    # Hum check kar rahe hain ki kya hamari API sahi se respond kar rahi hai
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}