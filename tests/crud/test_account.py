import pytest
from faker import Faker
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app import crud, schemas
from app.models.account import Account
from tests.config import settings_test

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_create_account(client: AsyncClient) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
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
async def test_get_accounts(client: AsyncClient) -> None:
    accounts_created = []
    accounts_to_create = 5
    for _ in range(accounts_to_create):
        account_name = faker_data.name()
        account_description = faker_data.paragraph()
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
async def test_get_account(client: AsyncClient) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_2 = await crud.account.get(_id=account.id)
    assert account_2
    assert type(account_2) is Account
    assert jsonable_encoder(account) == jsonable_encoder(account_2)


@pytest.mark.asyncio
async def test_get_account_by_name(client: AsyncClient) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_2 = await crud.account.get_by_name(name=account_name)
    assert account_2
    assert type(account_2) is Account
    assert jsonable_encoder(account) == jsonable_encoder(account_2)


@pytest.mark.asyncio
async def test_update_account(client: AsyncClient) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    new_account_name = faker_data.name()
    account_in_update = schemas.AccountUpdate(name=new_account_name)
    await crud.account._update(_id=account.id, obj_in=account_in_update)
    account_2 = await crud.account.get(_id=account.id)
    assert account_2
    assert type(account_2) is Account
    assert account.description == account_2.description
    assert account_2.name == new_account_name


@pytest.mark.asyncio
async def test_remove_account(client: AsyncClient) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_id = account.id
    account_deleted = await crud.account._remove(_id=account_id)
    found_account_removed = await crud.account.get(_id=account_id)
    assert account_deleted == 1
    assert not found_account_removed


@pytest.mark.asyncio
async def test_partial_remove_account(client: AsyncClient) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    account_id = account.id
    await crud.account.partial_remove(_id=account_id)
    found_account_removed = await crud.account.get(_id=account_id)
    assert type(found_account_removed) is Account
    assert hasattr(found_account_removed, "name")
    assert hasattr(found_account_removed, "description")
    assert found_account_removed.name == account_name
    assert found_account_removed.description == account_description
    assert not found_account_removed.is_active
