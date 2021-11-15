from typing import Any, Dict

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app.core.security import verify_password
from tests.config import settings_test
from tests.utils.user import (
    regular_user_email,
    regular_user_full_name,
    regular_user_phone_number,
)

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


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


@pytest.mark.asyncio
async def test_login_access_token_without_exists_user(
    client: AsyncClient, auto_init_db: Any
) -> None:
    login_data = {
        "username": faker_data.email(),
        "password": faker_data.password(length=12),
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/access-token", data=login_data
    )
    result = r.json()
    assert result["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_login_access_token_with_invalid_password(
    client: AsyncClient, auto_init_db: Any
) -> None:
    login_data = {
        "username": settings_test.FIRST_SUPER_ADMIN_EMAIL,
        "password": faker_data.password(length=12),
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/access-token", data=login_data
    )
    result = r.json()
    assert result["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_hash_password(
    client: AsyncClient,
    auto_init_db: Any,
    normal_user_token_headers: Dict[str, str],
) -> None:
    password = faker_data.password(length=12)
    data = {"password": password}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/hash-password", json=data
    )
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    result = r.json()
    assert verify_password(
        plain_password=password,
        hashed_password=result,
    )
