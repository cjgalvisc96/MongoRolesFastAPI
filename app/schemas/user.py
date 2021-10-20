from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr

from app.schemas.user_role import UserRole
from app.schemas.validators import ObjectId


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    full_name: str
    phone_number: str
    account_id: Union[str, ObjectId]

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: Optional[EmailStr]
    is_active: Optional[bool]
    full_name: Optional[str]
    phone_number: Optional[str]
    account_id: Optional[str]
    password: Optional[str]


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
