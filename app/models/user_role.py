from umongo import fields

from app.core.db import mongo_db
from app.models.base import Base


@mongo_db.db.register
class UserRole(Base):
    user_id = fields.ObjectIdField(allow_none=True, required=True)
    role_id = fields.ObjectIdField(allow_none=True, required=True)

    class Meta:
        collection_name = "user_roles"
