from bson import ObjectId


def is_valid_object_id(value):
    return ObjectId.is_valid(value)
