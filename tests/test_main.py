from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    r = client.get("/ping")
    assert r.status_code == 200
    assert "result" in r.json()
    assert r.json()["result"] == "pong"
