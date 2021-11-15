from typing import Any, List

from fastapi import APIRouter, Security

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=List[schemas.Role])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all available user roles.
    """
    roles = await crud.role.get_multi(skip=skip, limit=limit)
    return roles
