from umongo import fields, validate

from app.models.base import Base
from app.core.db import mongo_db


@mongo_db.db.register
class Account(Base):
    name = fields.StringField(validate=validate.Length(max=255), required=True)
    description = fields.StringField(
        validate=validate.Length(max=255), allow_none=True
    )
    plan_id = fields.ObjectIdField(allow_none=True)
    current_subscription_ends = fields.DateTimeField(allow_none=True)
    created_at = fields.DateTimeField(required=False)
    updated_at = fields.DateTimeField(required=False)

    class Meta:
        collection_name = "accounts"
