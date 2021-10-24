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
    async def get_with_role_and_account(cls, *, user_id: str):
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
            # join with user_role collection
            {
                "$lookup": {
                    "from": "user_roles",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "pipeline": [
                        {"$project": {"role_id": 1}},
                    ],
                    "as": "user_role",
                }
            },
            # create temp vars
            {"$addFields": {"temp_role_id": "$user_role.role_id"}},
            # join with role collection
            {
                "$lookup": {
                    "from": "roles",
                    "localField": "temp_role_id",
                    "foreignField": "_id",
                    "pipeline": [
                        {"$project": {"name": 1}},
                    ],
                    "as": "role",
                }
            },
            # remove innecesary temp vars
            {"$project": {"temp_role_id": 0}},
        ]
        user_with_role_and_account = {}
        cursor = cls.collection.aggregate(pipeline)
        async for document in cursor:
            user_with_role_and_account = document
        return user_with_role_and_account

    """
    from marshmallow import pre_load
    @pre_load(pass_many=False)
    def remove_envelope(self, data, many, **kwargs):
        data['user_role'] = {"hello": "world"}
        return data
    """
