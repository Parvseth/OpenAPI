from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_order():
    payload = {
        
        "id": 123,
        
        "petId": 123,
        
        "quantity": 123,
        
        "shipDate": "example_value",
        
        "status": [],
        
        "complete": True,
        
    }
    response = client.post("/orders", json=payload)  # ✅ Pluralized path
    assert response.status_code == 200

def test_get_all_orders():
    response = client.get("/orders")  # ✅ Pluralized path
    assert response.status_code == 200
    assert isinstance(response.json(), list)