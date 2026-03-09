from fastapi.testclient import TestClient

from openprecedent.api import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_schema_catalog_contains_core_objects() -> None:
    response = client.get("/schemas")

    assert response.status_code == 200
    body = response.json()
    assert "case" in body
    assert "event" in body
    assert "decision" in body
    assert "artifact" in body
    assert "precedent" in body
