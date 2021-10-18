from typing import Optional
from bson.objectid import ObjectId
from app.crud.base import CRUDBase
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def __init__(self):
        self.model = UserRole

    async def get_by_user_id(self, *, user_id: str) -> Optional[UserRole]:
        return await self.model.find_one({"user_id": ObjectId(user_id)})

user_role = CRUDUserRole()
