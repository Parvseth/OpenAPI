from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_():
    payload = {
        "id":
                    123,
        "category":
                    1,
        "name":
                    "doggie",
        "photoUrls":
                    "[]",
        "tags":
                    "[]",
        "status":
                    example_status,
    }
    response = client.post("/", json=payload)
    assert response.status_code == 200 or response.status_code == 201

def test_get_all_():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)