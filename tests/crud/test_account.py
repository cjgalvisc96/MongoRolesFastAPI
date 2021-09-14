import pytest
from app import crud, schemas
from app.models.account import Account
from tests.utils.utils import random_lower_string


@pytest.mark.asyncio
async def test_create_account(client) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
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
