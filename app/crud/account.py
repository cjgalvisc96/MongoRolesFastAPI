from app.crud.base import CRUDBase
from app.models.account import Account

class CRUDAccount(CRUDBase[Account]):
    pass

account = CRUDAccount(Account)