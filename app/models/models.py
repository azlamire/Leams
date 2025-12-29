from sqlalchemy.orm.strategy_options import defaultload
from sqlmodel import SQLModel, Field
from pydantic import IPvAnyAddress
import sqlmodel
from typing import Optional


# IDK: About one big table or having multiple small tables
# but I do think that needed small tables cause it will be
# so large data


class UserCreate(SQLModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    email: str = Field(default=None)
    birthday: str = Field(default=None)


class UserLogin(SQLModel):
    user_email: str = Field(default=None)
    password: str = Field(default=None)


# class Location(SQLModel,table=True):
#     id: int = Field(default=None, primary_key=True)
#     username: str = Field(default=None)
#     country: str = Field(default=None)
#     town: str = Field(default=None)
#     ip: IPvAnyAddress = Field(default=None)
#     os: str = Field(default=None)
class IsUser(SQLModel):
    nickname: str


class IsEmail(SQLModel):
    email: str


class UserRequest(SQLModel):
    id: int | None = Field(default=None, index=True, primary_key=True)
    username: str = Field(default=None)
    password: str = Field(default=None)
    email: str = Field(default=None)
