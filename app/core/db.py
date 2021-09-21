from abc import ABC
from typing import Optional
from umongo.frameworks import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient

class MongoAsync(ABC):
    def __init__(self, uri: str = None, db_name: str = None):
        self.uri: str = uri
        self.db_name: str = db_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorClient] = None
        self._instance = MotorAsyncIOInstance()

    def init_db(self):
        if not self.uri:
            raise ValueError("Database uri connection is not defined")
        if not self.db_name:
            raise ValueError("the database name is not defined")

        self._client = AsyncIOMotorClient(self.uri)
        self._db = self._client[self.db_name]
        self._instance.set_db(self._db)

    @property
    def db(self):
        """Return a umongo ODM db instance"""
        return self._instance

    @property
    def db_instance(self):
        """Return a pure mongodb instance"""
        return self._instance.db

mongo_db = MongoAsync()
