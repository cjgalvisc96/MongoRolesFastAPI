from umongo import fields, validate

from app.models.base import Base
from app.core.db import mongo_db


@mongo_db.db.register
class User(Base):
    full_name = fields.StringField(
        validate=validate.Length(max=255), required=True
    )
    email = fields.EmailField(
        validate=validate.Length(max=255), unique=True, required=True
    )
    phone_number = fields.StringField(
        validate=validate.Length(max=10), required=True
    )
    hashed_password = fields.StringField(
        validate=validate.Length(max=255), required=True
    )
    account_id = fields.ObjectIdField(allow_none=True, required=True)

    class Meta:
        collection_name = "users"
