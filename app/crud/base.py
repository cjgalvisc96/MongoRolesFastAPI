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
        objects = []
        cursor = self.model.find().sort("name", -1).skip(skip).limit(limit)
        async for document in cursor:
            objects.append(document)
        return objects

    async def get(self, *, _id: str) -> Optional[ModelType]:
        return await self.model.find_one({"_id": ObjectId(_id)})

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        await db_obj.commit()
        return db_obj

    async def _update(
        self,
        *,
        _id: str,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        obj_to_update = await self.get(_id=_id)
        obj_to_update.update(update_data)
        await obj_to_update.commit()
        return obj_to_update

    async def _remove(self, *, _id: str):
        self.model.remove({"_id": ObjectId(_id)})
        await self.model.commit()
        return None
