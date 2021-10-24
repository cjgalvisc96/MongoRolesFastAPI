from bson import ObjectId
from umongo import fields, validate

from app.core.db import mongo_db
from app.models.base import Base


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

    @classmethod
    def get_with_account_and_role(cls, *, user_id: str):
        pipeline = [
            {"$match": {"_id": ObjectId(user_id)}},
            # join with accounts collection
            {
                "$lookup": {
                    "from": "accounts",
                    "localField": "account_id",
                    "foreignField": "_id",
                    "pipeline": [
                        {"$project": {"name": 1}},
                    ],
                    "as": "account",
                }
            },
            {"$unwind": "$account"},
            # join with user_roles collection
            {
                "$lookup": {
                    "from": "user_roles",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "pipeline": [
                        {"$project": {"role_id": 1, "user_id": 1}},
                    ],
                    "as": "user_role",
                }
            },
            {"$unwind": "$user_role"},
            # join with roles collection
            {
                "$lookup": {
                    "from": "roles",
                    "let": {"role_id": "$user_role.role_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$role_id"]}}},
                        {"$project": {"name": 1}},
                    ],
                    "as": "role",
                }
            },
            {"$unwind": "$role"},
            {"$project": {"user_role": 0}},
        ]
        return cls.collection.aggregate(pipeline)

    """
    from marshmallow import pre_load
    @pre_load(pass_many=False)
    def remove_envelope(self, data, many, **kwargs):
        data['user_role'] = {"hello": "world"}
        return data
    """
