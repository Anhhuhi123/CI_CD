from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_200_and_ok_status() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_returns_200() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()