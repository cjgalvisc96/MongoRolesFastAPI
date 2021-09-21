from typing import Any, Dict, List, Optional, Union

from bson import ObjectId
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        self.model = User

    async def get_by_email(self, *, email: str) -> Optional[User]:
        return await self.model.find_one({"email": email})

    async def create(self, *, obj_in: UserCreate) -> User:
        obj_in.hashed_password = get_password_hash(obj_in.password)
        return await super().create(obj_in=obj_in)

    async def update(
        self,
        *,
        _id: str,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(_id=_id, obj_in=update_data)


    def authenticate(
        self,
        *, 
        email: str,
        password: str
    ) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    async def get_by_account_id(
        self,
        *,
        account_id: ObjectId,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        objects = []
        cursor = self.model.find({"account_id": account_id}).sort("name", -1).skip(skip).limit(limit)
        async for document in cursor:
            objects.append(document)
        return objects


user = CRUDUser()