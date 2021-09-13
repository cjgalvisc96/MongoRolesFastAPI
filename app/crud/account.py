from typing import Optional

from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def __init__(self):
        self.model = Account

    async def get_by_name(self, *, name: str) -> Optional[Account]:
        return await self.model.find_one({"name": name})


account = CRUDAccount()
