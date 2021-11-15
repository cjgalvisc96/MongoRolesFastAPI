from typing import Optional

from bson import ObjectId

from app import models, schemas


def is_valid_object_id(value):
    return ObjectId.is_valid(value)


def get_user_schema_with_role_and_account(
    *, user: models.User
) -> Optional[schemas.User]:
    if not (hasattr(user, "role") and hasattr(user, "account")):
        # GUEST user
        role = None
        account = None
    else:
        role = user.role
        account = user.role
    user = schemas.User(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        full_name=user.full_name,
        phone_number=user.phone_number,
        account_id=user.account_id,
        role=role,
        account=account,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    return user
