import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    r = await client.get("/ping")
    assert r.status_code == 200
    assert "result" in r.json()
    assert r.json()["result"] == "pong"
