from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Security
from starlette import status

from app import crud, models, schemas
from app.api import deps
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
            detail="An account with this name already exists",
        )
    account = await crud.account.create(obj_in=account_in)
    return account


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
            detail="Account does not exist",
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
            detail="Account does not exist",
        )
    account_users = await crud.user.get_by_account_id(
        account_id=account.id, skip=skip, limit=limit
    )
    return account_users
