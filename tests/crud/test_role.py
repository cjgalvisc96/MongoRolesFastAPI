import pytest
from faker import Faker
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app import crud, schemas
from app.models.role import Role
from tests.config import settings_test

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_create_role(client: AsyncClient) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    role = await crud.role.create(obj_in=role_in)
    assert type(role) is Role
    assert hasattr(role, "name")
    assert hasattr(role, "description")
    assert role.name == role_name
    assert role.description == role_description
    assert role.is_active


@pytest.mark.asyncio
async def test_get_roles(client: AsyncClient) -> None:
    roles_created = []
    roles_to_create = 5
    for _ in range(roles_to_create):
        role_name = faker_data.name()
        role_description = faker_data.paragraph()
        role_in = schemas.RoleCreate(
            name=role_name, description=role_description
        )
        role_created = await crud.role.create(obj_in=role_in)
        roles_created.append(role_created)
    roles = await crud.role.get_multi(skip=0, limit=roles_to_create)
    assert len(roles) == roles_to_create
    assert type(roles) is list
    assert type(roles[0]) is Role


@pytest.mark.asyncio
async def test_get_role(client: AsyncClient) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    role = await crud.role.create(obj_in=role_in)
    role_2 = await crud.role.get(_id=role.id)
    assert role_2
    assert type(role_2) is Role
    assert jsonable_encoder(role) == jsonable_encoder(role_2)


@pytest.mark.asyncio
async def test_get_role_by_name(client: AsyncClient) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    role = await crud.role.create(obj_in=role_in)
    role_2 = await crud.role.get_by_name(name=role_name)
    assert role_2
    assert type(role_2) is Role
    assert jsonable_encoder(role) == jsonable_encoder(role_2)


@pytest.mark.asyncio
async def test_update_role(client: AsyncClient) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    role = await crud.role.create(obj_in=role_in)
    new_role_name = faker_data.name()
    role_in_update = schemas.RoleUpdate(name=new_role_name)
    await crud.role._update(_id=role.id, obj_in=role_in_update)
    role_2 = await crud.role.get(_id=role.id)
    assert role_2
    assert type(role_2) is Role
    assert role.description == role_2.description
    assert role_2.name == new_role_name


@pytest.mark.asyncio
async def test_remove_role(client: AsyncClient) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    role = await crud.role.create(obj_in=role_in)
    role_id = role.id
    role_deleted = await crud.role._remove(_id=role_id)
    found_role_removed = await crud.role.get(_id=role_id)
    assert role_deleted == 1
    assert not found_role_removed


@pytest.mark.asyncio
async def test_partial_remove_role(client: AsyncClient) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    role = await crud.role.create(obj_in=role_in)
    role_id = role.id
    await crud.role.partial_remove(_id=role_id)
    found_role_removed = await crud.role.get(_id=role_id)
    assert type(found_role_removed) is Role
    assert hasattr(found_role_removed, "name")
    assert hasattr(found_role_removed, "description")
    assert found_role_removed.name == role_name
    assert found_role_removed.description == role_description
    assert not found_role_removed.is_active
