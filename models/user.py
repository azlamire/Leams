from pydantic import BaseModel, EmailStr
class UserSchema(BaseModel):
    username: str
    password: bytes
    email: EmailStr
    active: bool = True
