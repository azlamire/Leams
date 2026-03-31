from pydantic import BaseModel


class User(BaseModel):
    pass


class Moderator(User):
    pass


class Admin(User):
    pass
