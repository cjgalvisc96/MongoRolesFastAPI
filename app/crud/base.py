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
        cursor = (
            self.model.find({"is_active": True})
            .sort("name", -1)
            .skip(skip)
            .limit(limit)
        )
        async for document in cursor:
            objects.append(document)
        return objects

    async def get(self, *, _id: str) -> Optional[ModelType]:
        return await self.model.find_one(
            {"_id": ObjectId(_id), "is_active": True}
        )

    async def get_not_active(self, *, _id: str) -> Optional[ModelType]:
        return await self.model.find_one(
            {"_id": ObjectId(_id), "is_active": False}
        )

    async def get_by_name(self, *, name: str) -> Optional[ModelType]:
        return await self.model.find_one({"name": name, "is_active": True})

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        await db_obj.commit()
        assert db_obj.is_created
        return db_obj

    async def _update(
        self,
        *,
        _id: str,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.dict(exclude_unset=True)
        )
        obj_to_update = await self.get(_id=_id)
        obj_to_update.update(update_data)
        await obj_to_update.commit()
        return obj_to_update

    async def _remove(self, *, _id: str) -> int:
        find_object = await self.get(_id=_id)
        object_deleted = await find_object.delete()
        return object_deleted.deleted_count

    async def partial_remove(self, *, _id: str) -> ModelType:
        update_status = {"is_active": False}
        obj_to_update = await self.get(_id=_id)
        obj_to_update.update(update_status)
        await obj_to_update.commit()
        return obj_to_update
