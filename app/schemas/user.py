from datetime import datetime
from typing import Dict, Optional, Union

from pydantic import BaseModel, EmailStr, Field

from app.schemas.validators import ObjectId


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    full_name: str
    phone_number: str
    account_id: Optional[Union[str, ObjectId]]

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
    password: Optional[str]


class UserInDBBase(UserBase):
    id: Optional[ObjectId]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class UserRole(BaseModel):
    id: ObjectId = Field(alias="_id")
    name: str

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


class UserAccount(BaseModel):
    id: ObjectId = Field(alias="_id")
    name: str

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


class User(UserInDBBase):
    role: Optional[UserRole]
    account: Optional[UserAccount]


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    id: ObjectId = Field(alias="_id")
    hashed_password: str
    account: Optional[Dict]
    role: Optional[Dict]
