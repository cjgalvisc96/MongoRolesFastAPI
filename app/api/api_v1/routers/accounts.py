from typing import Any, List

from fastapi import APIRouter, HTTPException, Security
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role

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
