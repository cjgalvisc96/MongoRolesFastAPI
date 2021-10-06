from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.user_role import UserRole
from app.schemas.validators import ObjectId


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    full_name: str
    phone_number: str
    account_id: str

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: ObjectId
    user_role: Optional[UserRole]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
