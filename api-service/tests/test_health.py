from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint():
    response = TestClient(app).get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
