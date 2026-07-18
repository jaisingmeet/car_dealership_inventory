from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

# Har baar test chalne par purani tables delete karke fresh table banengi
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
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
    assert response.json() == {
        "message": "User registered successfully"
    }
def test_register_duplicate_email():
    user = {
        "username": "meet",
        "email": "meet@example.com",
        "password": "Password123"
    }

    # First registration
    client.post("/api/auth/register", json=user)

    # Duplicate registration
    response = client.post("/api/auth/register", json=user)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already registered"
    }
def test_database_session_exists():
    from app.database import SessionLocal

    session = SessionLocal()

    assert session is not None

    session.close()
from app.models import User


def test_user_model_exists():
    user = User(
        username="meet",
        email="meet@example.com",
        hashed_password="hashed_password"
    )

    assert user.username == "meet"
    assert user.email == "meet@example.com"
# backend/tests/test_auth.py ke end mein ye add karo:

def test_login_user_success():
    # Pehle ek fresh user data registration ke liye bhejte hain
    user_data = {
        "username": "login_test_user",
        "email": "login_test@example.com",
        "password": "SecurePassword123"
    }
    client.post("/api/auth/register", json=user_data)

    # Ab login karne ki koshish karte hain
    login_credentials = {
        "username": "login_test_user",
        "password": "SecurePassword123"
    }
    response = client.post("/api/auth/login", json=login_credentials)
    
    # Kyunki login route abhi tak bana hi nahi hai, ye fail hona chahiye
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
