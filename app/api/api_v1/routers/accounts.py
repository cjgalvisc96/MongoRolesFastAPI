from typing import Any
from fastapi import APIRouter, HTTPException
from starlette import status

from app import crud, schemas
router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=schemas.Account)
async def create_account(
    *,
    account_in: schemas.AccountCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    account = await crud.account.get_by_name(name=account_in.name)
    if account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this name already exists",
        )
    account = await crud.account.create(obj_in=account_in)
    return account
