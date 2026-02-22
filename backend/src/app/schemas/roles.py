from pydantic import BaseModel, EmailStr


class User(BaseModel):
    pass


class Moderator(User):
    pass


class Admin(User):
    pass
