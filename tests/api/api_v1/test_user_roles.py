from typing import Any, Dict

import pytest
from bson.objectid import ObjectId
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app import crud, models, schemas
from app.constants.role import Role
from tests.config import settings_test

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_assign_user_role(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    user_id = ObjectId()
    role_id = ObjectId()
    data = {
        "user_id": str(user_id),
        "role_id": str(role_id),
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/user-roles",
        headers=superadmin_token_headers,
        json=data,
    )
    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    user_role_created = r.json()
    user_role_found = await crud.user_role.get(_id=user_role_created["id"])
    assert type(user_role_found) is models.UserRole
    assert str(user_role_found.user_id) == user_role_created["user_id"]
    assert str(user_role_found.role_id) == user_role_created["role_id"]


@pytest.mark.asyncio
async def test_assign_user_role_with_exists_user_role(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    superadmin = await crud.user.get_by_email(
        email=settings_test.FIRST_SUPER_ADMIN_EMAIL
    )
    data = {
        "user_id": str(superadmin.id),
        "role_id": str(ObjectId()),
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/user-roles",
        headers=superadmin_token_headers,
        json=data,
    )
    assert status.HTTP_409_CONFLICT
    updated_user_role = r.json()
    expected_error_message = (
        f"User with id <<{superadmin.id}>> already has been assigned a role"
    )
    assert updated_user_role["detail"] == expected_error_message


@pytest.mark.asyncio
async def test_update_user_role(
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

    role = await crud.role.get_by_name(name=Role.ACCOUNT_MANAGER["name"])
    user_role_in = schemas.UserRoleCreate(
        user_id=str(user.id), role_id=str(role.id)
    )
    await crud.user_role.create(obj_in=user_role_in)
    new_role = await crud.role.get_by_name(name=Role.ACCOUNT_ADMIN["name"])
    data = {"role_id": str(new_role.id)}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/user-roles/{user.id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_user_role = r.json()
    assert 200 <= r.status_code < 300
    assert updated_user_role["role_id"] == str(new_role.id)


@pytest.mark.asyncio
async def test_update_user_role_without_exists_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    random_user_id = str(ObjectId())
    data = {"role_id": str(ObjectId())}
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/user-roles/{random_user_id}",
        headers=superadmin_token_headers,
        json=data,
    )
    assert status.HTTP_409_CONFLICT
    updated_user_role = r.json()
    expected_error_message = (
        f"There is no role assigned to this user with id <<{random_user_id}>>"
    )
    assert updated_user_role["detail"] == expected_error_message
