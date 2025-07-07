from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_():
    payload = {
        "id":
                    123,
        "petId":
                    123,
        "quantity":
                    123,
        "shipDate":
                    "example_shipDate",
        "status":
                    example_status,
        "complete":
                    True,
    }
    response = client.post("/", json=payload)
    assert response.status_code == 200 or response.status_code == 201

def test_get_all_():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)