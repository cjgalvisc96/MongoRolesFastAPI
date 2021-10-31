from typing import Any, List

from fastapi import APIRouter, HTTPException, Security
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[schemas.User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all users.
    """
    users = await crud.user.get_multi(
        skip=skip,
        limit=limit,
    )
    return users


@router.post("", response_model=schemas.User)
async def create_user(
    *,
    user_in: schemas.UserCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(obj_in=user_in)
    return user
