from services.inventory.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["service"] == "inventory"

def test_requires_auth():
    resp = client.get("/inventory/items")
    assert resp.status_code == 401
