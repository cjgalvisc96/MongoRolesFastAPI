from app.db.session import db_instance
from app.models.base import Base
from umongo import fields, validate


@db_instance.register
class Account(Base):
    name = fields.StringField(validate=validate.Length(max=255), required=True)
    description = fields.StringField(validate=validate.Length(max=255), allow_none=True)
    plan_id = fields.StringField(validate=validate.Length(min=5), allow_none=True)
    current_subscription_ends = fields.DateTimeField(allow_none=True)

    class Meta:
        collection_name = "accounts"
