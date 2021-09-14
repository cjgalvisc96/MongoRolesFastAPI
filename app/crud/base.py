from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.models.base import Base

# Define custom types for umongo model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return await self.model.find().skip(skip).limit(limit)

    async def get(self, *, _id: str) -> Optional[ModelType]:
        return await self.model.find_one({"_id": ObjectId(_id)})

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        await db_obj.commit()
        return db_obj

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        pass

    async def remove(self, *, _id: str) -> ModelType:
        db_obj = self.model.remove({"_id": ObjectId(_id)})
        await db_obj.commit()
        return db_obj
