from bson.objectid import ObjectId
import pytest
from faker import Faker
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app import crud, schemas
from app.models.user_role import UserRole
from tests.config import settings_test

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)

@pytest.mark.asyncio
async def test_create_user_role(client: AsyncClient) -> None:
    user_id = str(ObjectId())
    role_id = str(ObjectId())
    user_role_in = schemas.UserRoleCreate(
        user_id=user_id, role_id=role_id
    )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    assert type(user_role) is UserRole
    assert str(user_role.user_id) == user_id
    assert str(user_role.role_id) == role_id
    assert user_role.is_active


@pytest.mark.asyncio
async def test_get_user_roles(client: AsyncClient) -> None:
    user_roles_created = []
    user_roles_to_create = 5
    for _ in range(user_roles_to_create):
        user_id = str(ObjectId())
        role_id = str(ObjectId())
        user_role_in = schemas.UserRoleCreate(
            user_id=user_id, role_id=role_id
        )
        user_role_created = await crud.user_role.create(obj_in=user_role_in)
        user_roles_created.append(user_role_created)
    user_roles = await crud.user_role.get_multi(skip=0, limit=user_roles_to_create)
    assert len(user_roles) == user_roles_to_create
    assert type(user_roles) is list
    assert type(user_roles[0]) is UserRole


@pytest.mark.asyncio
async def test_get_user_role(client: AsyncClient) -> None:
    user_id = str(ObjectId())
    role_id = str(ObjectId())
    user_role_in = schemas.UserRoleCreate(
        user_id=user_id, role_id=role_id
    )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    user_role_2 = await crud.user_role.get(_id=user_role.id)
    assert user_role_2
    assert type(user_role_2) is UserRole
    assert jsonable_encoder(user_role) == jsonable_encoder(user_role_2)


@pytest.mark.asyncio
async def test_get_user_role_by_user_id(client: AsyncClient) -> None:
    user_id = str(ObjectId())
    role_id = str(ObjectId())
    user_role_in = schemas.UserRoleCreate(
        user_id=user_id, role_id=role_id
    )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    user_role_2 = await crud.user_role.get_by_user_id(user_id=user_id)
    assert user_role_2
    assert type(user_role_2) is UserRole
    assert jsonable_encoder(user_role) == jsonable_encoder(user_role_2)


@pytest.mark.asyncio
async def test_update_user_role(client: AsyncClient) -> None:
    user_id = str(ObjectId())
    role_id = str(ObjectId())
    user_role_in = schemas.UserRoleCreate(
        user_id=user_id, role_id=role_id
    )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    new_user_role_role_id = str(ObjectId())
    user_role_in_update = schemas.UserRoleUpdate(role_id=new_user_role_role_id)
    await crud.user_role._update(_id=user_role.id, obj_in=user_role_in_update)
    user_role_2 = await crud.user_role.get(_id=user_role.id)
    assert user_role_2
    assert type(user_role_2) is UserRole
    assert user_role.user_id == user_role_2.user_id
    assert str(user_role_2.role_id) == new_user_role_role_id


@pytest.mark.asyncio
async def test_remove_user_role(client: AsyncClient) -> None:
    user_id = str(ObjectId())
    role_id = str(ObjectId())
    user_role_in = schemas.UserRoleCreate(
        user_id=user_id, role_id=role_id
    )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    user_role_id = user_role.id
    user_role_deleted = await crud.user_role._remove(_id=user_role_id)
    found_user_role_removed = await crud.user_role.get(_id=user_role_id)
    assert user_role_deleted == 1
    assert not found_user_role_removed

@pytest.mark.asyncio
async def test_partial_remove_user_role(client: AsyncClient) -> None:
    user_id = str(ObjectId())
    role_id = str(ObjectId())
    user_role_in = schemas.UserRoleCreate(
        user_id=user_id, role_id=role_id
    )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    user_role_id = user_role.id
    await crud.user_role.partial_remove(_id=user_role_id)
    found_user_role_removed = await crud.user_role.get(_id=user_role_id)
    assert str(found_user_role_removed.user_id) == user_id
    assert str(found_user_role_removed.role_id) == role_id
    assert not found_user_role_removed.is_active
