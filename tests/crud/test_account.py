import pytest
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient

from app import crud, schemas
from app.models.account import Account
from tests.utils.utils import random_lower_string


@pytest.mark.asyncio
async def test_create_account(client: TestClient) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    assert type(account) is Account
    assert hasattr(account, "name")
    assert hasattr(account, "description")
    assert account.name == account_name
    assert account.description == account_description
    assert account.is_active


@pytest.mark.asyncio
async def test_get_account(client: TestClient) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_2 = await crud.account.get(_id=account.id)
    assert account_2
    assert type(account) is Account
    assert jsonable_encoder(account) == jsonable_encoder(account_2)


@pytest.mark.asyncio
async def test_get_account_by_name(client: TestClient) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_2 = await crud.account.get_by_name(name=account_name)
    assert account_2
    assert type(account) is Account
    assert jsonable_encoder(account) == jsonable_encoder(account_2)
