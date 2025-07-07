from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_apiresponse():
    payload = {
        
        "code": 123,
        
        "type": "example_value",
        
        "message": "example_value",
        
    }
    response = client.post("/apiresponses", json=payload)  # ✅ Pluralized path
    assert response.status_code == 200

def test_get_all_apiresponses():
    response = client.get("/apiresponses")  # ✅ Pluralized path
    assert response.status_code == 200
    assert isinstance(response.json(), list)