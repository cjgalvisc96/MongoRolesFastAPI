from typing import Optional, Union

from pydantic import BaseModel

from app.schemas.validators import ObjectId


# Shared properties
class UserRoleBase(BaseModel):
    user_id: Optional[Union[str, ObjectId]]
    role_id: Optional[Union[str, ObjectId]]


# Properties to receive via API on creation
class UserRoleCreate(UserRoleBase):
    pass


# Properties to receive via API on update
class UserRoleUpdate(BaseModel):
    role_id: str


class UserRoleInDBBase(UserRoleBase):
    id: Optional[ObjectId]

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class UserRole(UserRoleInDBBase):
    pass


class UserRoleInDB(UserRoleInDBBase):
    pass
