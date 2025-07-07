from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    payload = {
        
        "id": 123,
        
        "username": "example_value",
        
        "firstName": "example_value",
        
        "lastName": "example_value",
        
        "email": "example_value",
        
        "password": "example_value",
        
        "phone": "example_value",
        
        "userStatus": 123,
        
    }
    response = client.post("/users", json=payload)  # ✅ Pluralized path
    assert response.status_code == 200

def test_get_all_users():
    response = client.get("/users")  # ✅ Pluralized path
    assert response.status_code == 200
    assert isinstance(response.json(), list)