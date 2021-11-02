from typing import Any, Dict

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app import crud, schemas
from tests.config import settings_test
from tests.utils.validators import check_if_element_exists_in_list

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_get_all_roles_by_authorised_user(
    client: AsyncClient, auto_init_db: Any, superadmin_token_headers: Dict
) -> None:
    role_name = faker_data.name()
    role_description = faker_data.paragraph()
    role_in = schemas.RoleCreate(name=role_name, description=role_description)
    await crud.role.create(obj_in=role_in)

    r = await client.get(
        f"{settings_test.API_V1_PREFIX}/roles",
        headers=superadmin_token_headers,
    )

    assert (
        status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    )
    roles = r.json()
    role_created_in_auto_init_db = 5
    roles_created = 1
    assert len(roles) == roles_created + role_created_in_auto_init_db
    role_conditions = {"name": role_name, "description": role_description}
    assert check_if_element_exists_in_list(
        _list=roles, _conditions=role_conditions
    )
