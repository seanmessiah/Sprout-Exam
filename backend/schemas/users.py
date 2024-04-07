from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str


class ShowUserSchema(BaseModel):
    id: int
    username: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str