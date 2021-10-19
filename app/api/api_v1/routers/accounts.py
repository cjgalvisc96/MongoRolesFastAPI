from typing import Any, List

from fastapi import APIRouter, Security

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
