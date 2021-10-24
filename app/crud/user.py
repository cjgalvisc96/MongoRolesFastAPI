from typing import Any, Dict, List, Optional, Union

from bson import ObjectId

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        self.model = User

    async def get_by_email(self, *, email: str) -> Optional[User]:
        email_filter = {"email": email}
        user_with_account_and_role = await self._get_with_account_and_role(
            _filter=email_filter
        )
        if not user_with_account_and_role:
            guest_user = await self.model.find_one(email_filter)
            return guest_user

        return user_with_account_and_role

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

    async def _get_with_account_and_role(
        self, *, _filter: Dict
    ) -> Optional[User]:
        _match = {"$match": _filter}
        user_with_role_and_account = {}
        async for user_found in self.model.get_with_account_and_role(
            _match=_match
        ):
            user_with_role_and_account = UserInDB(**user_found)
        return user_with_role_and_account


user = CRUDUser()
