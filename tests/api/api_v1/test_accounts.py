from typing import Any, Dict

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app import crud, models, schemas
from app.schemas.validators import ObjectId
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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    created_account = r.json()
    account = await crud.account.get_by_name(name=account_name)
    assert type(account) is models.Account
    assert account.name == created_account["name"]
    assert account.description == created_account["description"]


@pytest.mark.asyncio
async def test_create_account_with_exists_name(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    await crud.account.create(obj_in=account_in)

    data = {"name": account_name, "description": faker_data.paragraph()}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts",
        headers=superadmin_token_headers,
        json=data,
    )
    assert status.HTTP_409_CONFLICT
    created_account = r.json()
    expected_error_message = (
        f"An account with name <<{account_name}>> already exists"
    )
    assert created_account["detail"] == expected_error_message


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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert user["account_id"] == str(account.id)


@pytest.mark.asyncio
async def test_add_user_to_account_without_exists_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    data = {"user_id": str(ObjectId())}
    random_account_id = str(ObjectId())
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts/{random_account_id}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    user = r.json()
    assert status.HTTP_404_NOT_FOUND
    expected_error_message = (
        f"Account with id <<{random_account_id}>> not exists"
    )
    assert user["detail"] == expected_error_message


@pytest.mark.asyncio
async def test_add_user_to_account_with_invalid_user_id(
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
    invalid_iser_id = str(faker_data.random_number(digits=10))
    data = {"user_id": invalid_iser_id}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts/{str(account.id)}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    user = r.json()
    assert status.HTTP_400_BAD_REQUEST
    assert user["detail"] == f"user_id <<{invalid_iser_id}>> invalid format"


@pytest.mark.asyncio
async def test_add_user_to_account_without_exists_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    account_name = faker_data.name()
    account_description = faker_data.paragraph()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = await crud.account.create(obj_in=account_in)
    random_user_id = str(ObjectId())
    data = {"user_id": random_user_id}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts/{str(account.id)}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    user = r.json()
    assert status.HTTP_404_NOT_FOUND
    assert user["detail"] == f"User with id <<{random_user_id}>> not exists"


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
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts/{account.id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_account = r.json()
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert updated_account["name"] == new_account_name


@pytest.mark.asyncio
async def test_update_account_without_exists_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    random_account_id = str(ObjectId())
    new_account_name = faker_data.name()
    data = {"name": new_account_name}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/accounts/{random_account_id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_account = r.json()
    assert status.HTTP_404_NOT_FOUND
    expected_error_message = (
        f"Account with id <<{random_account_id}>> not exists"
    )
    assert updated_account["detail"] == expected_error_message


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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert result["success"] == f"Account with id={account.id} removed"


@pytest.mark.asyncio
async def test_remove_account_without_exists_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    random_account_id = str(ObjectId())
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/accounts/{random_account_id}",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert status.HTTP_404_NOT_FOUND
    expected_error_message = (
        f"Account with id <<{random_account_id}>> not exists"
    )
    assert result["detail"] == expected_error_message


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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert not result.get("is_active")


@pytest.mark.asyncio
async def test_partial_remove_account_without_exists_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    random_account_id = str(ObjectId())
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/accounts/{random_account_id}/partial",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert status.HTTP_404_NOT_FOUND
    expected_error_message = (
        f"Account with id <<{random_account_id}>> not exists"
    )
    assert result["detail"] == expected_error_message


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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
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
async def test_get_users_for_account_without_exists_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    random_account_id = str(ObjectId())
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts/{random_account_id}/users",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert status.HTTP_404_NOT_FOUND
    expected_error_message = (
        f"Account with id <<{random_account_id}>> not exists"
    )
    assert result["detail"] == expected_error_message


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
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
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


@pytest.mark.asyncio
async def test_get_users_for_own_account_without_exists_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    superadmin_account = await crud.account.get_by_name(
        name=settings_test.FIRST_SUPER_ADMIN_ACCOUNT_NAME
    )
    await crud.account._remove(_id=str(superadmin_account.id))
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/accounts/users/me",
        headers=superadmin_token_headers,
    )
    users = r.json()
    assert status.HTTP_404_NOT_FOUND
    expected_error_message = (
        f"Account with id <<{superadmin_account.id}>> not exists"
    )
    assert users["detail"] == expected_error_message
