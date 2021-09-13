from umongo import fields, validate

from app.db.session import db_instance
from app.models.base import Base


@db_instance.register
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
