from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_serves_html():
    res = client.get("/")
    assert res.status_code == 200
    assert "ISP-412 Alt" in res.text


def test_crud_flow():
    # Create
    res = client.post("/api/items", json={"name": "alpha", "description": "first"})
    assert res.status_code == 201
    created = res.json()
    item_id = created["id"]

    # Read list
    res = client.get("/api/items")
    assert res.status_code == 200
    items = res.json()
    assert any(i.get("name") == "alpha" for i in items)

    # Read single
    res = client.get(f"/api/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "alpha"

    # Update
    res = client.put(f"/api/items/{item_id}", json={"name": "beta", "description": "second"})
    assert res.status_code == 200
    assert res.json()["name"] == "beta"

    # Delete
    res = client.delete(f"/api/items/{item_id}")
    assert res.status_code == 204

    # Not found after delete
    res = client.get(f"/api/items/{item_id}")
    assert res.status_code == 404


