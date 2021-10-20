from typing import Dict

from httpx import AsyncClient

from app import crud
from app.schemas.user import UserCreate
from tests.config import settings_test

regular_user_email = "tester@email.com"
regular_user_password = "supersecretpassword"
regular_user_full_name = "john doe"
regular_user_phone_number = "3101234567"


async def get_superadmin_token_headers(client: AsyncClient) -> Dict[str, str]:
    login_data = {
        "username": settings_test.FIRST_SUPER_ADMIN_EMAIL,
        "password": settings_test.FIRST_SUPER_ADMIN_PASSWORD,
    }
    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> Dict[str, str]:
    login_data = {"username": email, "password": password}

    r = await client.post(
        f"{settings_test.API_V1_PREFIX}/auth/access-token", data=login_data
    )
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def authentication_token_from_email(
    *, client: AsyncClient, email: str
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    user = await crud.user.get_by_email(email=email)
    if not user:
        account = await crud.account.get_by_name(
            name=settings_test.FIRST_SUPER_ADMIN_ACCOUNT_NAME
        )
        if not account:
            bad_authorization = {"Authorization": ""}
            return bad_authorization

        user_in_create = UserCreate(
            username=email,
            email=email,
            full_name=regular_user_full_name,
            password=regular_user_password,
            phone_number=regular_user_phone_number,
            account_id=str(account.id),
        )
        user = await crud.user.create(obj_in=user_in_create)

    return await user_authentication_headers(
        client=client, email=email, password=regular_user_password
    )
