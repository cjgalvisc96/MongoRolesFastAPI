from typing import Optional

from app import models


async def get_role_name_from_user(user_id: str) -> Optional[models.Role]:
    """
    If not found role, by default is "GUEST"
    """
    user = await models.User.get_with_role_and_account(user_id=user_id)
    role = user.get("role")
    if not role:
        return "GUEST"  # Default role

    return role[0]["name"]
