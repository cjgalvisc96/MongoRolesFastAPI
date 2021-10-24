from typing import Optional

from app import crud, models


async def get_role_name_from_user(user_id: str) -> Optional[models.Role]:
    deafult_role = "GUEST"
    user = await crud.user._get_with_account_and_role(user_id=user_id)
    if not user:
        return deafult_role

    role = user.get("role")
    if not role:
        return deafult_role

    return role["name"]
