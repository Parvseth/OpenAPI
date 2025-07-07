from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_category():
    payload = {
        
        "id": 123,
        
        "name": "example_value",
        
    }
    response = client.post("/categories", json=payload)  # ✅ Pluralized path
    assert response.status_code == 200

def test_get_all_categories():
    response = client.get("/categories")  # ✅ Pluralized path
    assert response.status_code == 200
    assert isinstance(response.json(), list)