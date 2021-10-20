import logging

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from pydantic import ValidationError

from app import crud, models, schemas
from app.constants.role import Role
from app.core import security
from app.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/access-token",
    scopes={
        Role.GUEST["name"]: Role.GUEST["description"],
        Role.ACCOUNT_ADMIN["name"]: Role.ACCOUNT_ADMIN["description"],
        Role.ACCOUNT_MANAGER["name"]: Role.ACCOUNT_MANAGER["description"],
        Role.ADMIN["name"]: Role.ADMIN["description"],
        Role.SUPER_ADMIN["name"]: Role.SUPER_ADMIN["description"],
    },
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(reusable_oauth2),
) -> models.User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        if payload.get("id") is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        logger.error("Error Decoding Token", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(_id=token_data.id)
    if not user:
        raise credentials_exception
    if security_scopes.scopes and not token_data.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    if (
        security_scopes.scopes
        and token_data.role not in security_scopes.scopes
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return user


async def get_current_active_user(
    current_user: models.User = Security(
        get_current_user,
        scopes=[],
    ),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
