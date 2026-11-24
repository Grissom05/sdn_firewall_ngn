from fastapi.testclient import TestClient

from src_controller.backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_unimplemented_firewall_endpoint_is_explicit():
    response = client.post(
        "/api/v1/firewall/rules",
        json={
            "name": "block ssh",
            "protocol": "tcp",
            "destination_port": 22,
        },
    )

    assert response.status_code == 501
    assert "not implemented" in response.json()["detail"]
