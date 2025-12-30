from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str | EmailStr
    password: str
