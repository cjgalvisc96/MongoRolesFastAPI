from typing import Optional
from app import crud, models

async def get_role_name_from_user(user_id: str) -> Optional[models.Role]:
    """
        If not found role, by default is "GUEST"
    """
    user_role = await crud.user_role.get_by_user_id(user_id=user_id)
    role = None
    if user_role:
        role = await crud.role.get(_id=str(user_role.role_id))   

    if not role:
        return "GUEST" # Default role

    return role.name
