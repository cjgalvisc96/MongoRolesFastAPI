from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from bson import ObjectId
from app.models.base import Base

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """Base class that can be extend by other action classes.
           Provides basic CRUD and listing operations.
        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model

    def get(self, _id: ObjectId) -> Optional[ModelType]:
        return self.model.find_one({'_id': _id})
