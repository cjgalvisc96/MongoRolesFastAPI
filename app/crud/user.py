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
        create_data = obj_in.dict(exclude_unset=True)
        create_data["hashed_password"] = get_password_hash(
            create_data["password"]
        )
        del create_data["password"]
        return await super().create(obj_in=create_data)

    async def _update(
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
        return await super()._update(_id=_id, obj_in=update_data)

    async def authenticate(
        self, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_by_account_id(
        self,
        *,
        account_id: ObjectId,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        users_found = (
            self.model.find({"account_id": account_id})
            .sort("name", -1)
            .skip(skip)
            .limit(limit)
        )
        response = [user_found async for user_found in users_found]
        return response


user = CRUDUser()
