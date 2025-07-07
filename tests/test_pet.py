from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_pet():
    payload = {
        
        "id": 123,
        
        "category": [],
        
        "name": "example_value",
        
        "photoUrls": [],
        
        "tags": [],
        
        "status": [],
        
    }
    response = client.post("/pets", json=payload)  # ✅ Pluralized path
    assert response.status_code == 200

def test_get_all_pets():
    response = client.get("/pets")  # ✅ Pluralized path
    assert response.status_code == 200
    assert isinstance(response.json(), list)