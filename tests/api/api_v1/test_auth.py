from typing import Any, Dict

import pytest
from httpx import AsyncClient

from tests.config import settings_test
from tests.utils.user import (
    regular_user_email,
    regular_user_full_name,
    regular_user_phone_number,
)


@pytest.mark.asyncio
async def test_use_access_token(
    client: AsyncClient,
    auto_init_db: Any,
    normal_user_token_headers: Dict[str, str],
) -> None:
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/test-token",
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result.get("email") == regular_user_email
    assert result.get("phone_number") == regular_user_phone_number
    assert result.get("full_name") == regular_user_full_name
