from typing import Dict, Optional

from app import crud, schemas
from app.constants.role import Role
from app.core.config import settings
from app.models.user import User


async def init_db() -> None:
    await create_superadmin_account()
    superadmin_user = await create_superadmin_user()
    await create_default_role(default_role=Role.GUEST)
    await create_default_role(default_role=Role.ACCOUNT_ADMIN)
    await create_default_role(default_role=Role.ACCOUNT_MANAGER)
    await create_default_role(default_role=Role.ADMIN)
    await create_default_role(default_role=Role.SUPER_ADMIN)
    await create_superadmin_user_role(superadmin_user=superadmin_user)


async def create_superadmin_account() -> None:
    account = await crud.account.get_by_name(
        name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
    )
    if not account:
        account_in = schemas.AccountCreate(
            name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME,
            description="superadmin account",
        )
        await crud.account.create(obj_in=account_in)


async def create_superadmin_user() -> User:
    user = await crud.user.get_by_email(email=settings.FIRST_SUPER_ADMIN_EMAIL)
    if not user:
        account = await crud.account.get_by_name(
            name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
        )
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPER_ADMIN_EMAIL,
            password=settings.FIRST_SUPER_ADMIN_PASSWORD,
            full_name=settings.FIRST_SUPER_ADMIN_EMAIL,
            phone_number=settings.FIRST_SUPER_ADMIN_PHONE_NUMBER,
            account_id=str(account.id),
        )
        user = await crud.user.create(obj_in=user_in)

    return user


async def create_default_role(default_role: Dict[str, str]) -> None:
    role = await crud.role.get_by_name(name=default_role["name"])
    if not role:
        guest_role_in = schemas.RoleCreate(
            name=default_role["name"], description=default_role["description"]
        )
        await crud.role.create(obj_in=guest_role_in)


async def create_superadmin_user_role(
    *, superadmin_user: Optional[User]
) -> None:
    user_role = await crud.user_role.get_by_user_id(user_id=superadmin_user.id)
    if not user_role:
        role = await crud.role.get_by_name(name=Role.SUPER_ADMIN["name"])
        user_role_in = schemas.UserRoleCreate(
            user_id=str(superadmin_user.id), role_id=str(role.id)
        )
        await crud.user_role.create(obj_in=user_role_in)
