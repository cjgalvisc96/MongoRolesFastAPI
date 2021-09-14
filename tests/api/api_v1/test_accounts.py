import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app import crud
from tests.config import settings_test
from tests.utils.utils import random_lower_string

@pytest.mark.asyncio
async def test_create_account(
    client: TestClient
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    data = {"name": account_name, "description": account_description}
    async with AsyncClient(app=client.app, base_url=client.base_url) as ac:
        r = await ac.post(f"{settings_test.API_V1_PREFIX}/accounts", json=data)

    assert 200 <= r.status_code < 300
    created_account = r.json()
    account = await crud.account.get_by_name(name=account_name)
    assert account
    assert account.name == created_account["name"]