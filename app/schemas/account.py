from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.validators import PyObjectId

# Shared properties
class AccountBase(BaseModel):
    name: str
    description: Optional[str]
    current_subscription_ends: Optional[datetime]
    plan_id: Optional[PyObjectId]
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    pass


# Properties to receive via API on update
class AccountUpdate(AccountBase):
    pass


class AccountInDBBase(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Account(AccountInDBBase):
    pass


class AccountInDB(AccountInDBBase):
    pass