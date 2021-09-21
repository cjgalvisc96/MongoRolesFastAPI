import pytest
from httpx import AsyncClient

from app import crud, schemas
from app.models.user import User
from tests.utils.utils import random_lower_string, random_email

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = await crud.user.create(obj_in=user_in)
    assert type(user) is User
    assert user.email == email
    assert hasattr(user, "hashed_password")
