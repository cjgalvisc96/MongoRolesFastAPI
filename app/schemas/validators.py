import bson


class ObjectId(bson.ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return cls(value)
        except bson.errors.InvalidId:
            raise ValueError("Not a valid ObjectId")
