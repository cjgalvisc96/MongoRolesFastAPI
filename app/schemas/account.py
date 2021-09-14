from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.validators import ObjectId


# Shared properties
class AccountBase(BaseModel):
    name: str
    description: Optional[str]
    current_subscription_ends: Optional[datetime]
    plan_id: Optional[ObjectId]
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    pass


# Properties to receive via API on update
class AccountUpdate(AccountBase):
    pass


class AccountInDBBase(AccountBase):
    id: ObjectId
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class Account(AccountInDBBase):
    pass


class AccountInDB(AccountInDBBase):
    pass
