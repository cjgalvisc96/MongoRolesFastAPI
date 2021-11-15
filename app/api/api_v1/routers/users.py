from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.error_messages import users_error_messages
from app.api.api_v1.success_messages import users_success_messages
from app.api.utils import get_user_schema_with_role_and_account
from app.constants.role import Role
from app.core.config import settings
from app.schemas.validators import ObjectId

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


@router.get("/me", response_model=schemas.User)
async def get_me_user(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return get_user_schema_with_role_and_account(user=current_user)


@router.post("/me", response_model=schemas.User)
async def update_me_user(
    *,
    full_name: str = Body(None),
    phone_number: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if phone_number is not None:
        user_in.phone_number = phone_number
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = await crud.user._update(_id=str(current_user.id), obj_in=user_in)
    return user


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
            detail=users_error_messages[
                "user_with_email_already_exists"
            ].format(email=user_in.email),
        )
    user = await crud.user.create(obj_in=user_in)
    return user


@router.post("/open", response_model=schemas.User)
async def create_user_open(
    *,
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=users_error_messages["created_user_open_not_allowed"],
        )
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=users_error_messages[
                "user_with_email_already_exists"
            ].format(email=user_in.email),
        )
    user = await crud.user.create(obj_in=user_in)
    return user


@router.delete("/{user_id}/partial", response_model=schemas.User)
async def remove_partial_user(
    *,
    user_id: ObjectId,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Remove an user.
    """
    user = await crud.user.get(_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=users_error_messages["user_not_exists"].format(
                user_id=user_id
            ),
        )
    removed_partial_user = await crud.user.partial_remove(_id=user_id)
    return removed_partial_user


@router.delete("/{user_id}", response_model=Dict)
async def remove_user(
    *,
    user_id: ObjectId,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Remove an user.
    """
    user = await crud.user.get(_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=users_error_messages["user_not_exists"].format(
                user_id=user_id
            ),
        )
    user_deleted = await crud.user._remove(_id=user_id)
    if user_deleted != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=users_error_messages["user_not_exists"].format(
                user_id=user_id
            ),
        )

    return {
        "success": users_success_messages["user_removed"].format(
            user_id=user_id
        ),
    }


@router.post("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    user_id: ObjectId,
    user_in: schemas.UserUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Update an user.
    """
    user = await crud.user.get(_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=users_error_messages["user_not_exists"].format(
                user_id=user_id
            ),
        )
    user = await crud.user._update(_id=user_id, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(
    user_id: ObjectId,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve one user by user_id.
    """
    user = await crud.user.get(_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=users_error_messages["user_not_exists"].format(
                user_id=user_id
            ),
        )
    return get_user_schema_with_role_and_account(user=user)
