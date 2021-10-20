import pytest

from typing import Dict

from httpx import AsyncClient

from tests.config import settings_test


@pytest.mark.asyncio
async def test_use_access_token(
    client: AsyncClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/test-token",
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result