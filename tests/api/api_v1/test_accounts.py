import pytest
from faker import Faker
from httpx import AsyncClient

from app import crud, schemas
from tests.config import settings_test

faker_data = Faker(locale=settings_test.FAKER_DATA_LOCATE)


@pytest.mark.asyncio
async def test_get_all_accounts_by_authorised_user(
    client: AsyncClient, superadmin_token_headers: dict
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
