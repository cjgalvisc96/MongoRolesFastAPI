from typing import Any

import pytest
from faker import Faker
from httpx import AsyncClient

from app import crud, models, schemas
from tests.config import settings_test

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_get_all_accounts_by_authorised_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account_name_2 = faker_data.name()
    account_description_2 = faker_data.paragraph()
    account_in_2 = schemas.AccountCreate(
        name=account_name_2, description=account_description_2
    )
    await crud.account.create(obj_in=account_in)
    await crud.account.create(obj_in=account_in_2)
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts",
        headers=superadmin_token_headers,
    )
    assert 200 <= r.status_code < 300
    accounts = r.json()
    account_created_in_auto_init_db = 1
    accounts_created = 2
    assert len(accounts) == accounts_created + account_created_in_auto_init_db
    assert next(
        account
        for account in accounts
        if (
            account["name"] == account_name
            and account["description"] == account_description
        )
    )
    assert next(
        account
        for account in accounts
        if (
            account["name"] == account_name_2
            and account["description"] == account_description_2
        )
    )


@pytest.mark.asyncio
async def test_create_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    data = {"name": account_name, "description": account_description}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts",
        headers=superadmin_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_account = r.json()
    account = await crud.account.get_by_name(name=account_name)
    assert type(account) is models.Account
    assert account.name == created_account["name"]
    assert account.description == created_account["description"]
