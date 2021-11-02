from typing import Any, Dict

import pytest
from bson.objectid import ObjectId
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app import crud, models, schemas
from tests.config import settings_test
from tests.utils.validators import check_if_element_exists_in_list

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_get_all_users_by_authorised_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    email = faker_data.email()
    email = faker_data.email()
    password = faker_data.password(length=12)
    full_name = faker_data.name()
    phone_number = faker_data.random_number(digits=10)
    account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        phone_number=phone_number,
        account_id=str(account_id),
    )
    await crud.user.create(obj_in=user_in)

    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/users",
        headers=superadmin_token_headers,
    )

    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    users = r.json()
    user_created_in_auto_init_db = 1
    users_created = 1
    assert len(users) == users_created + user_created_in_auto_init_db
    user_conditions = {
        "email": email,
        "full_name": full_name,
        "phone_number": str(phone_number),
        "account_id": str(account_id),
    }
    assert check_if_element_exists_in_list(
        _list=users, _conditions=user_conditions
    )


@pytest.mark.asyncio
async def test_create_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    email = faker_data.email()
    password = faker_data.password(length=12)
    full_name = faker_data.name()
    phone_number = faker_data.random_number(digits=10)
    account_id = ObjectId()
    data = {
        "email": email,
        "password": password,
        "full_name": full_name,
        "phone_number": phone_number,
        "account_id": str(account_id),
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    user_created = r.json()
    user_found = await crud.user.get_by_email(email=email)
    assert type(user_found) is models.User
    assert user_found.email == user_created["email"]
    assert user_found.full_name == user_created["full_name"]
    assert user_found.phone_number == user_created["phone_number"]
    assert str(user_found.account_id) == user_created["account_id"]


@pytest.mark.asyncio
async def test_partial_remove_account(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    email = faker_data.email()
    password = faker_data.password(length=12)
    full_name = faker_data.name()
    phone_number = faker_data.random_number(digits=10)
    account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        phone_number=phone_number,
        account_id=str(account_id),
    )
    user = await crud.user.create(obj_in=user_in)
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/users/{user.id}/partial",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert not result.get("is_active")


@pytest.mark.asyncio
async def test_partial_remove_account_not_user_exists(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    user_id_not_exists = str(ObjectId())
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/users/{user_id_not_exists}/partial",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert (
        result["detail"] == f"User wit id <<{user_id_not_exists}>> not exists"
    )


@pytest.mark.asyncio
async def test_remove_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    email = faker_data.email()
    password = faker_data.password(length=12)
    full_name = faker_data.name()
    phone_number = faker_data.random_number(digits=10)
    account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=email,
        password=password,
        full_name=full_name,
        phone_number=phone_number,
        account_id=str(account_id),
    )
    user = await crud.user.create(obj_in=user_in)
    r = await client.delete(
        f"{settings_test.API_V1_PREFIX}/users/{user.id}",
        headers=superadmin_token_headers,
    )
    result = r.json()
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert result["success"] == f"User with id <<{user.id}>> removed"
