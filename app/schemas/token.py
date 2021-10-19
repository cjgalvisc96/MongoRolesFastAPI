from pydantic import BaseModel
from app.schemas.validators import ObjectId

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: ObjectId
    role: str = None
    account_id: ObjectId = None
