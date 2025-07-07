from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_tag():
    payload = {
        
        "id": 123,
        
        "name": "example_value",
        
    }
    response = client.post("/tags", json=payload)  # ✅ Pluralized path
    assert response.status_code == 200

def test_get_all_tags():
    response = client.get("/tags")  # ✅ Pluralized path
    assert response.status_code == 200
    assert isinstance(response.json(), list)