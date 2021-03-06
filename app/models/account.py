from umongo import fields, validate

from app.core.db import mongo_db
from app.models.base import Base


@mongo_db.db.register
class Account(Base):
    name = fields.StringField(validate=validate.Length(max=255), required=True)
    description = fields.StringField(
        validate=validate.Length(max=255), allow_none=True
    )
    plan_id = fields.ObjectIdField(allow_none=True)
    current_subscription_ends = fields.DateTimeField(allow_none=True)

    class Meta:
        collection_name = "accounts"
