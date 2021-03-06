from typing import Optional

from pydantic import BaseModel

from app.schemas.validators import ObjectId


# Shared properties
class RoleBase(BaseModel):
    name: str
    description: Optional[str]


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: ObjectId

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class Role(RoleInDBBase):
    pass


class RoleInDB(RoleInDBBase):
    pass
