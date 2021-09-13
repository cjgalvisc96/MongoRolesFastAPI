from typing import Generic, Optional, TypeVar

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.models.base import Base

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    async def get(self, _id: ObjectId) -> Optional[ModelType]:
        return await self.model.find_one({"_id": ObjectId(_id)})

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        await db_obj.commit()
        return db_obj.dump()
