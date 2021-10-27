from typing import Any, Dict

import pytest
from faker import Faker
from httpx import AsyncClient

from app import crud, models, schemas
from tests.config import settings_test
from tests.utils.user import regular_user_email
from tests.utils.validators import check_if_element_exists_in_list

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_get_all_accounts_by_authorised_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
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
    account_conditions = {
        "name": account_name,
        "description": account_description,
    }
    assert check_if_element_exists_in_list(
        _list=accounts, _conditions=account_conditions
    )
    account_conditions_2 = {
        "name": account_name_2,
        "description": account_description_2,
    }
    assert check_if_element_exists_in_list(
        _list=accounts, _conditions=account_conditions_2
    )


@pytest.mark.asyncio
async def test_get_account_for_user(
    client: AsyncClient, auto_init_db: Any, normal_user_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    user = await crud.user.get_by_email(email=regular_user_email)
    user_in_update = schemas.UserUpdate(account_id=account.id)
    await crud.user._update(_id=user.id, obj_in=user_in_update)
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts/me",
        headers=normal_user_token_headers,
    )
    user_account = r.json()
    assert 200 <= r.status_code < 300
    assert user_account["id"] == str(account.id)


@pytest.mark.asyncio
async def test_create_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
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


@pytest.mark.asyncio
async def test_add_user_to_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    user = await crud.user.get_by_email(
        email=settings_test.FIRST_SUPER_ADMIN_EMAIL
    )
    data = {"user_id": str(user.id)}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts/{str(account.id)}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    user = r.json()
    assert 200 <= r.status_code < 300
    assert user["account_id"] == str(account.id)


@pytest.mark.asyncio
async def test_update_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    new_account_name = faker_data.name()
    data = {"name": new_account_name}
    r = await client.put(
        f"{settings_test.API_V1_PREFIX}/accounts/{account.id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_account = r.json()
    assert 200 <= r.status_code < 300
    assert updated_account["name"] == new_account_name


@pytest.mark.asyncio
async def test_remove_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/accounts/{account.id}",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert 200 <= r.status_code < 300
    assert result["success"] == f"Account with id={account.id} removed"


@pytest.mark.asyncio
async def test_partial_remove_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/accounts/{account.id}/partial",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert 200 <= r.status_code < 300
    assert not result.get("is_active")


@pytest.mark.asyncio
async def test_get_users_for_account_by_authorized_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    user_in = schemas.UserCreate(
        email=faker_data.email(),
        password=faker_data.password(length=12),
        full_name=faker_data.name(),
        phone_number=faker_data.random_number(digits=10),
        account_id=str(account.id),
    )
    user_in_2 = schemas.UserCreate(
        email=faker_data.email(),
        password=faker_data.password(length=12),
        full_name=faker_data.name(),
        phone_number=faker_data.random_number(digits=10),
        account_id=str(account.id),
    )
    await crud.user.create(obj_in=user_in)
    await crud.user.create(obj_in=user_in_2)
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts/{str(account.id)}/users",
        headers=superadmin_token_headers,
    )
    users = r.json()
    assert 200 <= r.status_code < 300
    assert len(users) == 2


@pytest.mark.asyncio
async def test_get_users_for_account_by_unauthorized_user(
    client: AsyncClient, auto_init_db: Any, normal_user_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts/{str(account.id)}/users",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 401
    result = r.json()
    assert result["detail"] == "Not enough permissions"


@pytest.mark.asyncio
async def test_get_users_for_own_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    user = await crud.user.get_by_email(
        email=settings_test.FIRST_SUPER_ADMIN_EMAIL
    )
    user_in = schemas.UserCreate(
        email=faker_data.email(),
        password=faker_data.password(length=12),
        full_name=faker_data.name(),
        phone_number=faker_data.random_number(digits=10),
        account_id=str(user.account_id),
    )
    user_in_2 = schemas.UserCreate(
        email=faker_data.email(),
        password=faker_data.password(length=12),
        full_name=faker_data.name(),
        phone_number=faker_data.random_number(digits=10),
        account_id=str(user.account_id),
    )
    await crud.user.create(obj_in=user_in)
    await crud.user.create(obj_in=user_in_2)
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts/users/me",
        headers=superadmin_token_headers,
    )
    assert 200 <= r.status_code < 300
    users = r.json()
    users_created_in_auto_init_db = 1
    users_created = 2
    assert len(users) == users_created + users_created_in_auto_init_db
    user_conditions = {"email": user_in.email}
    assert check_if_element_exists_in_list(
        _list=users, _conditions=user_conditions
    )
    user_conditions_2 = {"email": user_in_2.email}
    assert check_if_element_exists_in_list(
        _list=users, _conditions=user_conditions_2
    )
