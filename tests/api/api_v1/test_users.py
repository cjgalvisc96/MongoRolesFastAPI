from typing import Any, Dict

import pytest
from bson.objectid import ObjectId
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app import crud, models, schemas
from app.core.security import verify_password
from tests.config import settings_test
from tests.utils.user import regular_user_email
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
async def test_get_user_by_id(
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

    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/users/{user.id}",
        headers=superadmin_token_headers,
    )

    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    user = r.json()
    assert type(user) is dict
    user_conditions = {
        "email": email,
        "full_name": full_name,
        "phone_number": str(phone_number),
        "account_id": str(account_id),
    }
    assert check_if_element_exists_in_list(
        _list=[user], _conditions=user_conditions
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
async def test_partial_remove_user(
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
async def test_partial_remove_user_not_user_exists(
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


@pytest.mark.asyncio
async def test_update_user(
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

    new_user_email = faker_data.email()
    new_user_password = faker_data.password(length=12)
    new_user_full_name = faker_data.name()
    new_user_phone_number = faker_data.random_number(digits=10)
    data = dict(
        email=new_user_email,
        password=new_user_password,
        full_name=new_user_full_name,
        phone_number=new_user_phone_number,
    )

    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/users/{user.id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_user = r.json()
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    assert updated_user["email"] == new_user_email
    assert updated_user["full_name"] == new_user_full_name
    assert updated_user["phone_number"] == str(new_user_phone_number)
    user_found = await crud.user.get_by_email(email=new_user_email)
    assert verify_password(
        plain_password=new_user_password,
        hashed_password=user_found.hashed_password,
    )


@pytest.mark.asyncio
async def test_create_user_open(
    client: AsyncClient, auto_init_db: Any, normal_user_token_headers: Dict
) -> None:
    email = faker_data.email()
    password = faker_data.password(length=12)
    full_name = faker_data.name()
    phone_number = faker_data.random_number(digits=10)
    data = {
        "email": email,
        "password": password,
        "full_name": full_name,
        "phone_number": phone_number,
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/users/open",
        headers=normal_user_token_headers,
        json=data,
    )
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    user_open_created = r.json()
    user_found = await crud.user.get_by_email(email=email)
    assert type(user_found) is models.User
    assert user_found.email == user_open_created["email"]
    assert user_found.full_name == user_open_created["full_name"]
    assert user_found.phone_number == user_open_created["phone_number"]
    assert not user_found.account_id
    assert verify_password(
        plain_password=password,
        hashed_password=user_found.hashed_password,
    )


@pytest.mark.asyncio
async def test_get_me_user_super_admin(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/users/me",
        headers=superadmin_token_headers,
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == settings_test.FIRST_SUPER_ADMIN_EMAIL
    assert current_user["role"]
    assert current_user["account"]


@pytest.mark.asyncio
async def test_get_me_user_normal_user(
    client: AsyncClient, auto_init_db: Any, normal_user_token_headers: Dict
) -> None:
    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/users/me",
        headers=normal_user_token_headers,
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == regular_user_email
    assert not current_user["role"]
    assert not current_user["account"]
