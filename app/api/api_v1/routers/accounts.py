from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.error_messages import (
    account_error_messages,
    users_error_messages,
)
from app.api.utils import is_valid_object_id
from app.constants.role import Role
from app.schemas.validators import ObjectId

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=List[schemas.Account])
async def get_accounts(
    *,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all accounts.
    """
    accounts = await crud.account.get_multi(skip=skip, limit=limit)
    return accounts


@router.get("/me", response_model=schemas.Account)
async def get_account_for_user(
    *,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve account for a logged in user.
    """
    account = await crud.account.get(_id=current_user.account_id)
    return account


@router.post("", response_model=schemas.Account)
async def create_account(
    *,
    account_in: schemas.AccountCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create an user account
    """
    account = await crud.account.get_by_name(name=account_in.name)
    if account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=account_error_messages[
                "account_with_name_already_exists"
            ].format(name=account_in.name),
        )
    account = await crud.account.create(obj_in=account_in)
    return account


@router.post("/{account_id}/users", response_model=schemas.User)
async def add_user_to_account(
    *,
    account_id: ObjectId,
    user_id: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a user to an account.
    """
    account = await crud.account.get(_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=account_error_messages["account_not_exists"].format(
                account_id=account_id
            ),
        )

    if not is_valid_object_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=users_error_messages["invalid_format_user_id"].format(
                user_id=user_id
            ),
        )

    user = await crud.user.get(_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=users_error_messages["user_not_exists"].format(
                user_id=user_id
            ),
        )
    user_in = schemas.UserUpdate(account_id=account_id)
    updated_user = await crud.user._update(_id=user_id, obj_in=user_in)
    return updated_user


@router.post("/{account_id}", response_model=schemas.Account)
async def update_account(
    *,
    account_id: ObjectId,
    account_in: schemas.AccountUpdate,
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
    Update an account.
    """
    # If user is an account admin, check ensure they update their own account.
    if (
        hasattr(current_user, "role")
        and current_user.role.get("name") == Role.ACCOUNT_ADMIN["name"]
        and current_user.account_id != account_id
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=account_error_messages[
                "user_without_permissions_to_update_account"
            ].format(user_id=current_user.id),
        )
    account = await crud.account.get(_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=account_error_messages["account_not_exists"].format(
                account_id=account_id
            ),
        )
    account = await crud.account._update(_id=account_id, obj_in=account_in)
    return account


@router.delete("/{account_id}", response_model=Dict)
async def remove_account(
    *,
    account_id: ObjectId,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Remove an account.
    """
    account = await crud.account.get(_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=account_error_messages["account_not_exists"].format(
                account_id=account_id
            ),
        )
    account_deleted = await crud.account._remove(_id=account_id)
    if account_deleted != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not is possible remove the account with id={account_id}",
        )

    return {
        "success": f"Account with id={account_id} removed",
    }


@router.delete("/{account_id}/partial", response_model=schemas.Account)
async def remove_partial_account(
    *,
    account_id: ObjectId,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Remove an account.
    """
    account = await crud.account.get(_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=account_error_messages["account_not_exists"].format(
                account_id=account_id
            ),
        )
    account_deleted = await crud.account.partial_remove(_id=account_id)
    return account_deleted


@router.get("/{account_id}/users", response_model=List[schemas.User])
async def retrieve_users_for_account(
    *,
    skip: int = 0,
    limit: int = 100,
    account_id: ObjectId,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve users for an account.
    """
    account = await crud.account.get(_id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=account_error_messages["account_not_exists"].format(
                account_id=account_id
            ),
        )
    account_users = await crud.user.get_by_account_id(
        account_id=account_id, skip=skip, limit=limit
    )
    return account_users


@router.get("/users/me", response_model=List[schemas.User])
async def retrieve_users_for_own_account(
    *,
    skip: int = 0,
    limit: int = 100,
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
    Retrieve users for own account.
    """
    account = await crud.account.get(_id=current_user.account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=account_error_messages["account_not_exists"].format(
                account_id=current_user.account_id
            ),
        )
    account_users = await crud.user.get_by_account_id(
        account_id=account.id, skip=skip, limit=limit
    )
    return account_users
