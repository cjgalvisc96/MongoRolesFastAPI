from typing import Any

from fastapi import APIRouter, HTTPException, Security
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.error_messages import user_roles_error_messages
from app.constants.role import Role
from app.schemas.validators import ObjectId

router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("", response_model=schemas.UserRole)
async def assign_user_role(
    *,
    user_role_in: schemas.UserRoleCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ACCOUNT_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Assign a role to a user after creation of a user
    """
    user_role = await crud.user_role.get_by_user_id(
        user_id=user_role_in.user_id
    )
    if user_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=user_roles_error_messages[
                "user_roles_already_exists_for_user"
            ].format(user_id=user_role_in.user_id),
        )
    user_role = await crud.user_role.create(obj_in=user_role_in)
    return user_role


@router.post("/{user_id}", response_model=schemas.UserRole)
async def update_user_role(
    *,
    user_id: ObjectId,
    user_role_in: schemas.UserRoleUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ACCOUNT_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Update a user role.
    """
    user_role = await crud.user_role.get_by_user_id(user_id=user_id)
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_roles_error_messages[
                "invalid_assigned_user_role"
            ].format(user_id=user_id),
        )
    user_role_updated = await crud.user_role._update(
        _id=str(user_role.id), obj_in=user_role_in
    )
    return user_role_updated
