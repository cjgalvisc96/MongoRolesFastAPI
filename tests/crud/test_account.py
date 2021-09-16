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
async def test_get_accounts(client: TestClient) -> None:
    accounts_created = []
    accounts_to_create = 5
    for _ in range(accounts_to_create):
        account_name = random_lower_string()
        account_description = random_lower_string()
        account_in = schemas.AccountCreate(
            name=account_name, description=account_description
        )
        account_created = await crud.account.create(obj_in=account_in)
        accounts_created.append(account_created)
    accounts = await crud.account.get_multi(skip=0, limit=accounts_to_create)
    assert len(accounts) == accounts_to_create
    assert type(accounts) is list
    assert type(accounts[0]) is Account


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


@pytest.mark.asyncio
async def test_update_account(client: TestClient) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    new_account_name = random_lower_string()
    account_in_update = schemas.AccountUpdate(name=new_account_name)
    await crud.account._update(_id=account.id, obj_in=account_in_update)
    account_2 = await crud.account.get(_id=account.id)
    assert account_2
    assert type(account) is Account
    assert account.description == account_2.description
    assert account_2.name == new_account_name


@pytest.mark.asyncio
async def test_remove_account(client: TestClient) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_id = account.id
    account_deleted = await crud.account._remove(_id=account_id)
    found_account_removed = await crud.account.get(_id=account_id)
    assert account_deleted == 1
    assert not found_account_removed
